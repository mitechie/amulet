
import os
import json
import glob
import json_rpc
import cherrypy


class Module (object):
    @json_rpc.expose_anonymous
    def relations(self):
        if not cherrypy.request.method == "GET":
            raise cherrypy.HTTPError(405)

        if not os.path.exists('/opt/relations'):
            return {}

        relations = {}
        for relation in glob.glob('/opt/relations/*'):
            relname = os.path.basename(relation)
            relations[relname] = self.list_units(relname)

        return relations

    @json_rpc.expose_anonymous
    def relation(self, relation=None, unit=None):
        if not cherrypy.request.method == 'GET':
            raise cherrypy.HTTPError(405)

        if not relation:
            raise cherrypy.HTTPError(400)

        if not os.path.exists(os.path.join('/opt/relations', relation)):
            raise cherrypy.HTTPError(404)

        if not unit:
            data = {}
            for unit in self.list_units(relation):
                data[unit] = json.loads(self.relation(relation, unit).decode())
            return data

        data_file = os.path.join('/opt/relations', relation, unit, 'data')
        if not os.path.exists(data_file):
            raise cherrypy.HTTPError(404)

        with open(data_file, 'r') as u:
            unit_data = json.loads(u.read())

        return unit_data

    def list_units(self, relation):
        units = []
        for relunits in glob.glob('/opt/relations/%s/*' % relation):
            units.append(os.path.basename(relunits))

        return units
