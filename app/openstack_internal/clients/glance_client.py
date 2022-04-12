from openstack_internal.clients.clients import Clients


class Glance:

    def __init__(self, clients: Clients):
        self.__clients = clients.get_glance_client()

    def get_image_list(self):
        images_list = []
        for _image in self.__clients.images.list():
            images_list.append(_image)
        return images_list

    def get_images_by_wildcard_name(self, name):
        _images = []
        for _image in self.get_image_list():
            if (_image.get('name') and name in _image.get('name')) or\
                    (_image.get('description') and name in _image.get('description')):
                _images.append(_image)
        return _images

    def get_image_id(self, name):
        for image in self.get_image_list():
            if name in image.get('name'):
                return image.get('id')


def main():
    glance = Glance(Clients())
    image_name = "bionic-server-cloudimg-amd64"
    for image in glance.get_image_list():
        print("Image name {}: {}".format(image.get('name'), image.keys()))
    for image in glance.get_images_by_wildcard_name("server"):
        print("selected image {}: {}".format(image.get('name'), image.get('description')))
    print("Id of image {} is {}".format(image_name, glance.get_image_id(image_name)))


if __name__ == "__main__":
    main()

"""
glance = Clients().get_glance_client()
print('glanceClient: {}'.format(type(glance)))
images = glance.images.list()

print('Images type: {}'.format(type(images)))
print('Images dir: {}'.format(dir(images)))
print('Images list: {}'.format(images))

for image in images:
    print('Image Type: ', type(image))
    # model = warlock.core.model_factory(schema=Schema(raw_schema='glance'))
    # print('model {}'.format(model))
    print('Image dir: ', dir(image))
    print('Image keys: ', image.keys())

    print('Image name: ', image.get('name'))
    for key in image.keys():
        print("Image {}: {}".format(key, image.get(key)))

    print('-------------------------------------------\n')
    break

# print(list(images))

"""
