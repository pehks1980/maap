#python script to update image container name for the service
import ruamel.yaml
import argparse

parser = argparse.ArgumentParser(
    description='It looks for docker-compose.yml then updates it with arguments, finally new updated file *.new is created.'''
)
parser.add_argument("svc", help="service to update",
                    type=str, nargs='?', default='')
parser.add_argument("key", help="key in service svc to update",
                    type=str, nargs='?', default='image')
parser.add_argument("val", help="new value of the key",
                    type=str, nargs='?', default='')
args = parser.parse_args()

print("given: ", args.svc, args.key, args.val)

file_name = 'docker-compose.yml'
config, ind, bsi = ruamel.yaml.util.load_yaml_guess_indent(open(file_name))

services = config['services']
patched = False
for service in services:
    print(service)
    if service == args.svc:
        print("found service: ", service, "patched with value: ",args.val, "previous val was:", services[args.svc][args.key])
        services[args.svc][args.key] = args.val
        patched = True

if patched:
    yaml = ruamel.yaml.YAML()
    yaml.indent(mapping=ind, sequence=ind, offset=bsi)
    with open('docker-compose.yml', 'w') as fp:
        yaml.dump(config, fp)
else:
    print("couldn't find what to patch...")
    print("given: ", args.svc, args.key, args.val)
