import datetime
import uuid
import requests
import json
from decouple import config
import logging

log = logging.getLogger('byneuron')

class Byneuron:
    def __init__(self):
        self.api = f'{config("BYNEURON_URL")}/api/v1'
        self._token = ''
        self._token_expire = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
        self._publicIdTypes = None
        self._isc = None
        # load indexSets for user and set one as default
        self.indexSets = self.get_indexsets()
        self.indexSetActive = self.indexSets[0]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            log.error("Error Type: {}, \nError: {}\n".format(exc_type.__name__, exc_val))

    @property
    def now(self):
        """timezone aware utc now"""
        return datetime.datetime.now(datetime.timezone.utc)

    @property
    def headers(self):
        """default header for API"""
        return {'Authorization': 'Bearer {}'.format(self.token)}

    @property
    def token(self):
        """triggers login if needed"""
        if self.now > self._token_expire:
            data = self._login()
            if data:
                log.debug('set _token from data \n%s ', json.dumps(data, indent=2))
                self._token = data.get('access_token', '')
                self._token_expire = self.now + datetime.timedelta(seconds=data.get('expires_in', 0))
        return self._token

    def url(self, url, headers=None, data=None, as_json=True):
        log.info('requests url %s', url)
        if headers is None:
            headers = self.headers
        if isinstance(data, dict):
            if as_json:
                log.debug('request.post json \n%s \n%s \n%s', url, headers, data)
                r = requests.post(url, headers=headers, json=data)
            else:
                r = requests.post(url, headers=headers, data=data)
                log.debug('request.post data \n%s \n%s \n%s', url, headers, data)
        else:
            r = requests.get(url, headers=headers)
            log.debug('request.get \n%s \n%s', url, headers)

        if r.status_code == 200:
            return r.json()  # returns a dict
        else:
            r.raise_for_status()

    def set_indexset(self, e, verbose=True):
        """analogy of selecting a tenant in frontend"""
        if isinstance(e, Entity) and e.entity_type == 'IndexSet':
            if verbose:
                log.info('Welcome to tenant %s', e.name)
            self.indexSetActive = e

    def iter_indexset(self):
        for e in self.indexSets:
            self.set_indexset(e, True)
            yield self.indexSetActive

    def publicids(self, entitytype):
        if self._publicIdTypes is None:
            self._publicIdTypes = [e.entity_type_ref for e in self.get_entities('PublicId') if isinstance(e, Entity)]
            log.info('publicids', self._publicIdTypes)
        return entitytype in self._publicIdTypes

    ### endpoints ##
    def _login(self):
        login_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            "client_id": config('OAUTH2_CLIENT_ID'),
            "client_secret": config('OAUTH2_CLIENT_SECRET'),
            "grant_type": "client_credentials"
        }
        url = config('KEYCLOAK_TOKEN_URL')
        r = self.url(url=url, headers=login_headers, data=data, as_json=False)
        return r

    def _datamodel(self):
        url = f'{self.api}/backend/rest/datamodel'
        return self.url(url=url)

    def _graphql(self, query, references=None):
        """
        graphql query array eg ["CodeType:?codeTypes entity:type CodeType."]
        default retrieve ?indexSet
        :returns {'codeTypes':{'id':{object}}}
        """
        query = "\n".join(query) if isinstance(query, list) else f'{query}'
        references = references if isinstance(references, dict) else {}
        data = {
            "query": query,
            "references": references
        }
        url = f'{self.api}/backend/rest/datamodel/_graphql'
        log.info('_graphql %s', data)
        return self.url(url=url, data=data)

    def _graphmodel(self, entities=None, events=None):
        """ create / edit entities and events into the model"""
        nodes = {e.key: e.wrap() for e in entities if isinstance(e, Entity)} \
            if isinstance(entities, list) else {}
        events = [e.wrap() for e in events if isinstance(e, Numberevent)] \
            if isinstance(events, list) else []
        data = {
            "entityDataModel": {"nodes": nodes},
            "numberEventDataModel": {"events": events}
        }
        log.info('graphmodel, data: \n%s', json.dumps(data, indent=2))
        url = f'{self.api}/backend/tasks/entities/graphmodel'
        return self.url(url=url, data=data)

    def _publicid(self, entitytype, indexset=None):
        if self.publicids(entitytype):
            data = {
                "indexSet": indexset.key if indexset else self.indexSetActive.key,
                "entityType": f'com.bynubian.shared.entities.{entitytype}',
                "fieldName": 'publicId',
                "date": self.now.strftime('%Y-%m-%d')
            }
            url = f'{self.api}/backend/rest/publicids/generate'
            r = self.url(url=url, data=data)
            if r:
                return r.get('publicId')

    def _numberevents(self, size=100, order="DESC", deleted=False, indexsets=None, filters=None):
        """
        :param size:
        :param order:
        :param deleted:
        :param indexsets: list of indexSet or entity keys, else active indexSet
        :param filters:
        :return:
        """
        if isinstance(indexsets, list):
            if all([isinstance(i, Entity) for i in indexsets]):
                indexsets = [i.key for i in indexsets]
            else:
                indexsets = indexsets
        else:
            indexsets = [self.indexSetActive.key]
        filters = [] if not isinstance(filters, list) else filters
        data = {
            "indexSets": indexsets,  # list of indexSet keys
            "order": order,  # "ASC","DESC"
            "size": int(size),
            "deleted": bool(deleted),
            "filters": filters,
            "esDocumentType": "NumberEvent"
        }

        url = f'{self.api}/backend/rest/numberevents/_query'
        return self.url(url=url, data=data)

    ### endpoint handlers ###
    def get_numberevents(self, item, size):
        """ last 100 events for item in {datetime:value} format """
        items = item if isinstance(item, list) else [item]
        f = {
            "type": "eventitemid",
            "values": [i.key if isinstance(i, Entity) else i for i in items],
            "invertFilter": False,
            "operator": "or"
        }
        indexsets = list({i.indexset for i in items if isinstance(i, Entity)})
        data = self._numberevents(indexsets=indexsets, filters=[f], size=size)
        if data:
            for i in data:
                yield Numberevent(node=i)

    def get_numberevents_dict(self, item, size):
        return {e.datetime: e.value for e in self.get_numberevents(item=item, size=size)}

    def query(self, query, keys):
        """
        Query a nuql expression and extract the entities for the requested variable
        note behaviour on result:
          keys = 'x' > result = {entities_for_x} ;
          keys = ['x'] > result = {'x': {entities_for_x}}
          keys = ['x','y'] > result = {'x': {entities_for_x}, 'y': {entities_for_y}}
        careful for large requests, use limit and offset is advised
        :param query: [] of lines for graphql
        :param keys: the [] of str variable(s)
        :return: {variable: {entityKey: Entity}} or {entityKey: Entity}
        """
        result = {}
        result_with_keys = isinstance(keys, list)
        data = self._graphql(query)
        if data:
            log.info('time _graphql %sms', data.get('time'))
            variables = data.get('variables', {})
            nodes = data.get('nodes', {})
            for k in keys if result_with_keys else [keys]:
                result.update({k: {}})
                for entityKey in variables.get(f"?{k}", []):
                    e = nodes.get(entityKey, {})
                    result[k].update({entityKey: Entity(node=e)})
        return result if result_with_keys else result.get(keys)

    def get_entities(self, entitytype, indexset=None, **kwargs):
        """
        iterates entities using a filter e.g. get_entities('Item', 'hydrobox', 'externalId':'regex:0/1/.*'}
        constructs the required nuql query
        :param entitytype: eg Item, Device, ..
        :param indexset:
            True, search all indexSets;
            None, search selected indexSet;
            string or [str], search indexSets by attribute-name
        """

        def from_kwarg(kwarg_key):
            v = kwargs.get(kwarg_key)
            if isinstance(v, str):
                return f'regex:"{v[6:]}"' if v.startswith('regex:') else f'"{v}"'
            elif isinstance(v, list):
                return f'{[i for i in v]}'
            elif v is True:
                return f'value:any'
            elif v is None:
                return f'value:none'

        if indexset is True:
            entity_list = self.indexSets  # all indexSets
        elif isinstance(indexset, list):
            entity_list = [i for i in indexset if isinstance(i, Entity)]  # specify multiple indexSets
        elif isinstance(indexset, str):
            entity_list = [i for i in self.indexSets if i.name == indexset or i.key == indexset]
        else:
            entity_list = [self.indexSetActive]  # default to active indexSet
        query = [
            f"IndexSet:?indexSet entity:key {[i.key for i in entity_list]}.",
            f"{entitytype}:?e link:{'isAssignedTo' if entitytype == 'Gateway' else 'isDefinedIn'} ?indexSet."
        ]
        filter_list = []
        for k in ['key']:
            if k in kwargs:
                filter_list.append(f'entity:{k} {from_kwarg(k)}')
        for k in ['name', 'externalId', 'publicId', 'codeType']:
            if k in kwargs:
                filter_list.append(f'attribute:{k} {from_kwarg(k)}')
        if filter_list:
            query.append(f"{entitytype}:?e {'; '.join(filter_list)}.")
        offset, limit = 0, 20
        while True:
            query.append(f"{entitytype}:?e limit {limit}; offset {offset}.")
            entities = self.query(query, 'e')
            for e in entities.values():
                if isinstance(e, Entity):
                    yield e
            if len(entities) < limit:
                break
            query.pop()  # remove limit
            offset += limit

    def get_entity(self, entitytype, **kwargs):
        for i in self.get_entities(entitytype, **kwargs):
            return i

    def get_indexsets(self):
        q = ['IndexSet:?indexSet attribute:name value:any.']
        r = self.query(q, 'indexSet')
        return [e for e in r.values() if isinstance(e, Entity)]

    def create_entity(self, entity):
        log.info('create_entity %s', entity)
        entity.set_context('create')
        log.info('create_entity %s %s %s', entity.entity_type, entity.role, entity.type)
        if not entity.entity_type == 'Gateway':

            # indexSetCode only for entity that are defined in indexSet
            if entity.role:
                for role in entity.role:
                    self.set_isc(f'{entity.entity_type.lower()}Role', role)
            if entity.type:
                self.set_isc(f'{entity.entity_type.lower()}Type', entity.type)

        data = self._graphmodel(entities=[entity])
        if data:
            log.info('created entity data %s', data)
            result = data.get('result', {}).get('entityDataModel', {}).get('nodes', {}).get(entity.key, {})
            log.info('created entity %s', result)
            return Entity(node=result)

    def update_entity(self, entity):
        entity.set_context('update')
        data = self._graphmodel(entities=[entity])
        if data:
            result = data.get('result', {}).get('entityDataModel', {}).get('nodes', {}).get(entity.key, {})
            return Entity(node=result)

    def create_item(self, **kwargs):

        # to filter the keywords we can allow, and to set required fields
        item_config = {
            'description': kwargs.get('description'),
            'name': kwargs.get('name'),
            'externalId': kwargs.get('externalId'),
            'publicId': self._publicid(entitytype="Item"),
            'active': True,
            'valid': True,
            'valueType': 'Double',
            'unit': kwargs.get('unit'),  # optional
            'data': kwargs.get('data'),  # optional
            'metaKeywords': kwargs.get('metaKeywords'),  # optional
            'metaBooleans': kwargs.get('metaBooleans'),  # optional
            'roles': kwargs.get('roles', ['DEFAULT']),
            'type': kwargs.get('type', 'DEFAULT')
        }
        e = Entity().create('Item', self.indexSetActive, **{k: v for k, v in item_config.items() if v is not None})
        return self.create_entity(e)

    def create_device(self, **kwargs):
        device_config = {
            'description': kwargs.get('description'),
            'name': kwargs.get('name'),
            'externalId': kwargs.get('externalId'),
            'publicId': self._publicid(entitytype="Device"),
            'active': True,
            'valid': True,
            'data': kwargs.get('data'),  # optional
            'metaKeywords': kwargs.get('metaKeywords'),  # optional
            'metaBooleans': kwargs.get('metaBooleans'),  # optional
            'roles': kwargs.get('roles', ['DEFAULT']),
            'type': kwargs.get('type', 'DEFAULT')
        }

        e = Entity().create('Device', self.indexSetActive, **{k: v for k, v in device_config.items() if v is not None})
        if kwargs.get('definition'):
            # add Definition using Exid, if not present, duplicate from different indexSet
            local = self.get_entity('DeviceDefinition', externalId=kwargs.get('definition'))
            if local is None:

                remote = self.get_entity('DeviceDefinition', indexSet=True, externalId=kwargs.get('definition'))
                if isinstance(remote, Entity):
                    log.info('duplicate definition %s', kwargs.get('definition'))
                    local = self.duplicate(remote, self.indexSetActive)
            if local:
                e.set_link('isImplementationOf', local)
        # todo add profile, assetModel, status
        return self.create_entity(e)

    def create_code(self, codetype, code):
        e = Entity().create('IndexSetCode', self.indexSetActive, codeType=codetype, code=code, key=f'{codetype}#{code}')
        self.create_entity(e)

    def create_codetype(self, codetype, parent_codetype=None):
        e = Entity().create('IndexSetCodeType', self.indexSetActive, key=codetype)
        if parent_codetype:
            pct = self.get_entity('IndexSetCodeType', key=parent_codetype)
            if isinstance(pct, Entity):
                e.set_link('hasParent', pct)
        self.create_entity(e)

    def set_features(self, parent, children):
        """
        :param parent: Entity of type Device, Site to create hasFeature-relation in
        :param children: [] of Entity of type Item to create hasFeature-relation to
        :return: parent after update
        """
        for child in children:
            parent.set_link('hasFeature', child)
        return self.update_entity(parent)

    def duplicate(self, entity, indexset):
        """
        duplicate an entity to a different indexSet
        :param entity: Entity to copy
        :param indexset: indexSet (Entity) to copy to
        :return:
        """
        e = Entity().create(
            entity.entity_type,
            indexset,
            description=entity.description,
            name=entity.name,
            externalId=entity.external_id,
            data=entity.data,
            metaKeywords=entity.meta_keywords,
            metaBooleans=entity.meta_booleans)
        log.info('new entity %s from copy %s', e, entity)
        return self.create_entity(e)

    def set_isc(self, codetype, code):
        """
        routine to make sure codetypes#code are available in entity creation
        buffers codes per codetype
        todo crete codetype relation to root > reference-data
        :param codetype: eg itemRole
        :param code: eg DEFAULT
        :return:
        """
        if self._isc is None:
            self._isc = {}
        if self.indexSetActive != self._isc.get('indexSet'):
            log.info('initiate indexSetBuffer')
            self._isc = {'indexSet': self.indexSetActive}
            for e in self.get_entities('IndexSetCodeType'):
                self._isc.update({e.key: None})

        if codetype not in self._isc:
            self.create_codetype(codetype, 'reference-data')
            self._isc.update({codetype: None})
            # create codetype
            # buffer the code e.g. DEFAULT for the codetype e.g. itemRole
        if not self._isc.get(codetype):
            # buffer existing codes
            self._isc.update({codetype: [e.code for e in self.get_entities('IndexSetCode', codeType=codetype)]})
        if code not in self._isc.get(codetype, []):
            self.create_code(codetype, code)
            self._isc[codetype].append(code)
            # create code

        log.info('buffered indexSetCodetypes %s', self._isc)
        # buffer existing codes


class Entity:
    def __init__(self, node=None):
        self._datamodel = {} if not isinstance(node, dict) else node

    def __repr__(self):
        return f'{self.entity_type} {self.name}'

    def wrap(self):
        return self._datamodel

    def _prop(self, key):
        return self._datamodel.get(key)

    def _attr(self, name):
        for a in self._datamodel.get('attributes', []):
            if a.get('name') == name:
                for k in a:
                    if k.endswith('Value') or k.endswith('Values'):
                        return a.get(k)

    def _link(self, linktype):
        for link in self._datamodel.get('links', []):
            if link.get('linktype') == linktype:
                return link.get('entityKey')

    @staticmethod
    def tail(s):
        seperator = ['#', '.']
        if isinstance(s, str):
            for i in seperator:
                if s.count(i):
                    return s.split(i)[-1]

    @property
    def key(self):
        return self._prop('key')

    @property
    def id(self):
        return self._prop('id')

    @property
    def entity_type(self):
        return self.tail(self._prop('type'))

    @property
    def entity_type_ref(self):
        # for publicId
        return self.tail(self._attr('entityTypeRef'))

    @property
    def entity_type_long(self):
        return self._prop('type')

    @property
    def description(self):
        return self._prop('description')

    @property
    def name(self):
        return self._attr('name')

    @property
    def external_id(self):
        return self._attr('externalId')

    @property
    def public_id(self):
        return self._attr('publicId')

    @property
    def unit(self):
        return self._attr('unit')

    @property
    def codetype(self):  # for indexSetCode
        return self._attr('codeType')

    @property
    def code(self):  # for indexSetCode
        return self._attr('code')

    @property
    def data(self):
        try:
            return json.loads(self._attr('data'))
        except json.JSONDecoder:
            log.exception('decode entity data')

    @property
    def meta_keywords(self):
        meta = self._attr('metaKeywords')
        if isinstance(meta, list):
            return {i.get('key'): i.get('value') for i in meta}

    @property
    def meta_booleans(self):
        meta = self._attr('metaBooleans')
        if isinstance(meta, list):
            return {i.get('key'): bool(i.get('value')) for i in meta}

    @property
    def role(self):
        roles = self._attr(f'{self.entity_type.lower()}Role')
        if isinstance(roles, list):
            return [self.tail(i) for i in roles]

    @property
    def roles(self):
        return self.role

    @property
    def type(self):
        t = self._attr(f'{self.entity_type.lower()}Type')
        if t:
            return self.tail(t)

    @property
    def indexset(self):
        if self.entity_type == 'Gateway':
            return self._link('isAssignedTo')
        return self._link('isDefinedIn')

    def create(self, entitytype, indexset, **kwargs):
        new_id = str(uuid.uuid4())
        key = kwargs.get('key', new_id)  # method to overwrite key, eg for indexSetCodeType
        self._datamodel = {
            "type": f'com.bynubian.shared.entities.{entitytype}',
            "id": new_id,
            "key": key,
            "links": [],
            "attributes": []
        }
        self.set_context('create')
        linktype = 'isAssignedTo' if self.entity_type == 'Gateway' else 'isDefinedIn'
        self.set_link(linktype, indexset)
        for k, v in kwargs.items():
            if v is None:
                continue
            elif k in ['description']:
                self._datamodel.update({k: v})
            else:
                self.set_attribute(k, v)
        return self

    def set_context(self, action):
        if 'entityContext' not in self._datamodel:
            self._datamodel.update({'entityContext': {}})
        if 'action' not in self._datamodel['entityContext']:
            self._datamodel['entityContext'].update({"action": action})

    def set_link(self, linktype, entity):
        def _index():
            for position, _link in enumerate(self._datamodel['links']):
                if _link.get('entityKey') == entity.key:
                    return position

        if 'links' not in self._datamodel:
            self._datamodel.update({'links': []})
        i = _index()
        if linktype is None:  # method to remove
            if i is not None:
                self._datamodel['links'].pop(i)
        elif isinstance(entity, Entity) and entity.key:
            log.info('setlink %s with %s / %s ', linktype, entity, entity.indexset)
            link = {
                "linkType": linktype,  # hasFeature
                "label": f'{linktype}{entity.entity_type}',  # hasFeatureItem
                'entityKey': entity.key,
                'entityId': entity.id,
                'entityType': entity.entity_type_long,
                'entityIndexSetKey': entity._link('isDefinedIn'),
                'entityIndexSetId': entity._link('isDefinedIn')
            }
            link = {k: v for k, v in link.items() if
                    v is not None}  # this will remove entityIndexSetKey for gateway and indexset entities
            if i is None:
                self._datamodel['links'].append(link)
            else:
                self._datamodel['links'][i] = link

    def set_attribute(self, name, value):
        def _index(attr_name):
            for position, _attr in enumerate(self._datamodel.get('attributes', [])):
                if _attr.get('name') == attr_name:
                    return position

        def _attribute(attr_name, attr_value, attr_entity, attr_type):
            return {  # , "com.bynubian.shared.Boolean", "numberValue", name, int(bool(value)))
                "name": attr_name,
                "type": f'com.bynubian.shared.{attr_entity}',
                attr_type: attr_value
            }

        if 'attributes' not in self._datamodel:
            self._datamodel.update({'attributes': []})
        # set value to None to have the attribute deleted
        if value is None:
            i = _index(name)
            if i is not None:
                self._datamodel['attributes'].pop(i)
            return
        try:
            if name in ['name', 'externalId', 'publicId', 'code']:
                attr = _attribute(name, str(value), 'Keyword', 'keywordValue')
            elif name in ['active', 'valid']:
                attr = _attribute(name, int(bool(value)), 'Boolean', 'numberValue')
            elif name in ['valueType']:
                attr = _attribute(name, str(value), 'ValueType', 'keywordValue')
            elif name in ['data']:
                attr = _attribute(name, json.dumps(value), 'Json', 'textValue')
            elif name in ['unit']:
                attr = _attribute(name, str(value), 'Unit', 'keywordValue')
            elif name in ['metaKeywords']:
                list_values = [{'key': k, 'value': str(v)} for k, v in value.items()] \
                    if isinstance(value, dict) else []
                attr = _attribute(name, list_values, 'ExtensionKeyword', 'extensionKeywordValues')
            elif name in ['metaBooleans']:
                list_values = [{'key': k, 'value': int(bool(v))} for k, v in value.items()] \
                    if isinstance(value, dict) else []
                attr = _attribute(name, list_values, 'ExtensionBoolean', 'extensionNumberValues')
            elif name in ['codeType']:
                attr = _attribute(name, str(value), 'IndexSetCodeType', 'keywordValue')
            elif name.endswith('Role'):
                # this is used in relations with single roles
                # e.g. name itemRole, value DEFAULT
                attr = _attribute(name, f'{name}#{value}', 'IndexSetCode', 'keywordValue')
            elif name in ['roles']:
                name = f'{self.entity_type.lower()}Role'
                list_roles = [f'{name}#{role}' for role in value]
                attr = _attribute(name, list_roles, 'IndexSetCode', 'keywordValues')
            elif name in ['type']:
                name = f'{self.entity_type.lower()}Type'
                type_value = f'{name}#{value}'
                attr = _attribute(name, type_value, 'IndexSetCode', 'keywordValue')
            else:
                return
            i = _index(name)
            if i is None:
                self._datamodel['attributes'].append(attr)
            else:
                self._datamodel['attributes'][i] = attr

        except (Exception,):
            log.exception('set_attribute')


class Numberevent:

    def __init__(self, node=None):
        if isinstance(node, dict):
            for k, v in node.items():
                setattr(self, k, v)

    def __repr__(self):
        return f'Numberevent {self.datetime} {self.value}'

    def wrap(self):
        return vars(self)

    def create(self, value, dt, item):
        """
        create the required attributes to populate the Event
        :param value: the numberValue that will be floated
        :param dt: datetime, either tz-aware or utc
        :param item: the Item-entity to link the event with
        :return:
        """

        def timestamp():
            # if not timezone aware; force UTC
            if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
                dt.replace(tzinfo=datetime.timezone.utc)
            return dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        node = {
            "timestamp": timestamp(),
            "id": str(uuid.uuid4()),  # todo is this needed
            "itemId": item.key,
            "documentType": "NumberEvent",
            "eventContext": {
                "action": "create"
            },
            "indexSetKey": item.indexset,
            "numberValue": float(value)
        }
        for key, value in node.items():
            setattr(self, key, value)

    @property
    def datetime(self):
        if hasattr(self, 'timestamp'):
            return datetime.datetime.strptime(self.timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')

    @property
    def value(self):
        if hasattr(self, 'numberValue'):
            return float(self.numberValue)

    @property
    def now(self):
        """timezone aware utc now"""
        return datetime.datetime.now(datetime.timezone.utc)


def example01():
    logging.basicConfig(level=logging.INFO)
    log.info('list tenants')
    # list tenants
    with Byneuron() as r:
        print(f'IndexSets in this environment: {[e.name for e in r.indexSets]}')


def example02():
    logging.basicConfig(level=logging.INFO)
    log.info('create item')
    # crete item 'test' in indexSet 0
    with Byneuron() as r:
        r.create_item(name='test')


if __name__ == '__main__':
    example02()
