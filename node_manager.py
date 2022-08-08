from source.util.database import Database
from source.util.timekeeper import Timestamps
from source.util.settings import Settings


class Nodes:
    def __init__(self, database_obj=None):
        self.ts = Timestamps()
        self.config = Settings('general.config')
        if database_obj is None:
            self.db = Database(self.config.get_setting('databases', 'nodes_db_path'))
        else:
            self.db = database_obj

    def add_node(self, node_id, status, lat, lon, node_config: dict = None, notes=None):
        existing_record = self.db.get_data_single_field('node_id', node_id)
        if len(existing_record) > 0:
            return False
        dataobj = {
            'node_id': node_id,
            'status': status,
            'lat': lat,
            'lon': lon,
            'node_config': node_config,
            'notes': notes,
            'date_created': self.ts.get_timestamp(),
            'date_last_modified': self.ts.get_timestamp()
        }
        self.db.insert(dataobj)
        return True

    def add_node_dataobj(self, node_config_dataobj):
        self.db.insert(node_config_dataobj)

    def remove_node(self, node_id):
        dataobj = {
            'node_id': node_id
        }
        removed_ids = self.db.remove_single_record(dataobj)
        if len(removed_ids) > 0:
            return True
        return False

    def update_node_status(self, node_id, status):
        current_config = self.db.get_data_single_field('node_id', node_id)
        if len(current_config) > 0:
            current_config = current_config[0]
            current_config['status'] = status
            current_config['date_last_modified'] = self.ts.get_timestamp()
            self.remove_node(node_id)
            self.add_node_dataobj(current_config)
            return True
        return False


def main():
    nodes = Nodes()
    # Adds dev prototype node
    print(nodes.add_node(2222631473, 'active', 28.606798, -81.200847, node_config={'sensors': True, 'camera': False},
                         notes='Hand wired prototype'))
    print(nodes.add_node(4144723677, 'active', 28.602916, -81.192481, node_config={'sensors': True, 'camera': False},
                         notes='First engineering sample'))
    print(nodes.add_node(4146216805, 'active', 28.592791, -81.200135, node_config={'sensors': True, 'camera': True},
                         notes='Second engineering sample'))
    print(nodes.add_node(4144717489, 'active', 28.602000, -81.206240, node_config={'sensors': True, 'camera': True},
                         notes='Third engineering sample'))
    # print(nodes.remove_node(2222631473))
    # Adds proto 1 node
    # nodes.add_node(4144723677, 'active', 28.316450, -80.726982)


if __name__ == '__main__':
    main()
