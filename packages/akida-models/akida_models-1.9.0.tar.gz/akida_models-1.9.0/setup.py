from os import path
from setuptools import setup, find_packages

# Read the contents of the README file
directory = path.abspath(path.dirname(__file__))
with open(path.join(directory, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='akida_models',
      version='1.9.0',
      description='Akida Models',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Kevin Tsiknos',
      author_email='ktsiknos@brainchip.com',
      url='https://doc.brainchipinc.com',
      license='Apache 2.0',
      license_files=['LICENSE', 'LICENSE.3rdparty'],
      packages=find_packages(),
      entry_points={
        'console_scripts': [
            'akida_models = akida_models.cli:main',
            'utk_face_train = akida_models.utk_face.utk_face_train:main',
            'kws_train = akida_models.kws.kws_train:main',
            'modelnet40_train = akida_models.modelnet40.modelnet40_train:main',
            'yolo_train = akida_models.detection.yolo_train:main',
            'dvs_train = akida_models.dvs.dvs_train:main',
            'mnist_train = akida_models.mnist.mnist_train:main',
            'imagenet_train = akida_models.imagenet.imagenet_train:main',
            'portrait128_train = akida_models.portrait128.portrait128_train:main',
            'centernet_train = akida_models.centernet.centernet_train:main',
            'tenn_dvs128_train = akida_models.tenn_spatiotemporal.dvs128_train:main',
            'tenn_eye_train = akida_models.tenn_spatiotemporal.eye_train:main',
            'tenn_jester_train = akida_models.tenn_spatiotemporal.jester_train:main'
        ]
      },
      install_requires=['cnn2snn~=2.15.0', 'quantizeml~=0.18.0', 'scipy', 'opencv-python<4.12',
        'mtcnn==0.1.1', 'imgaug', 'trimesh', 'librosa', 'tqdm', 'soundata', 'tonic'],
      python_requires='>=3.9')
