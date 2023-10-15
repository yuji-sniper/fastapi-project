import yaml

# with open('config.yml', 'w') as file:
#     yaml.dump({
#         'web_server': {
#             'host': '127.0.0.1',
#             'port': 80,
#         },
#         'db_server': {
#             'host': '127.0.0.1',
#             'port': 3306,
#         },
#     }, file)

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)
    print(data, type(data))
    print(data['web_server']['port'])
