import source.util.shared_config as cfg



def main():
    cfg.mesh_requests.append({'command_id': 1, 'priority': 5, 'status': 'incomplete', 'command': 'get_sensor_data',
                              'node_id': 4144723677})
    # comm = Comm()
    # comm.handle_commands()


if __name__ == '__main__':
    main()
