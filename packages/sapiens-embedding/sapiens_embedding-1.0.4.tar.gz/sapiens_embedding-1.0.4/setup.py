# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
from setuptools import setup, find_packages
package_name = 'sapiens_embedding'
version = '1.0.4'
setup(
    name=package_name,
    version=version,
    author='SAPIENS TECHNOLOGY',
    packages=find_packages(),
    install_requires=['sapiens-tokenizer==1.1.3'],
    url='https://github.com/sapiens-technology/SapiensEmbedding',
    license='Proprietary Software',
    include_package_data=True
)
# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
