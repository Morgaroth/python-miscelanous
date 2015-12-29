#!/usr/bin/env python3

# require toposort: pip install toposort
# require docker-py: pip install docker-py
import time

try:
    from docker import Client
except ImportError:
    print("Docker API module not found, may You should install it? \"pip install docker-py\"")
    raise

try:
    from toposort import toposort_flatten
except ImportError:
    print("toposort module not found, may You should install it? \"pip install toposort\"")
    raise

docker = Client(base_url='unix://var/run/docker.sock', version='auto')

too_old_in_days = 14

containers = docker.containers(all=True)
old_border = int(time.time()) - too_old_in_days * 24 * 60 * 60
newer_containers = [container for container in containers if container[u'Created'] > old_border]
older_containers = [container for container in containers if container[u'Created'] <= old_border]
for old in older_containers:
    try:
        docker.remove_container(old[u'Id'])
        print("Container removed %s" % old[u'Id'])
    except Exception as e:
        print("Cannot remove container %s because %s" % (old[u'Id'], e))

raw_images = docker.images(all=True)
images = {}
orphans = [i for i in raw_images if i[u'ParentId'] == u'']
print("Orphans: %s" % orphans)
for orphan in orphans:
    docker.remove_image(orphan[u'Id'])
    print("Orphan deleted %s" % orphan[u'Id'])

for i in [{i[u'Id']: {i[u'ParentId']}} for i in raw_images if i[u'ParentId'] != u'']:
    images.update(i)
images = toposort_flatten(images)
print("There is %d images to be removed." % len(images))
for i in images:
    try:
        docker.remove_image(str(i))
        print("Removed image %s." % str(i))
    except Exception as e:
        print("Image %s cannot be removed because %s" % (i, e))