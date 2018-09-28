rom setuptools import setup, find_packages

#   NOTE: pip-tools is not compatible with pip >= 10.0.0
#   While the issue above is being fixed, we commented out the following block and
#   instead used the block after for compiling the list of reqs.
#   https://github.com/jazzband/pip-tools/issues/648
# import pip
# NOTE: this is temporary until pip and pip-tools resolve the issue above.
def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

install_reqs = parse_requirements("requirements.txt")
reqs = [str(ir) for ir in install_reqs]


setup(
        name='step3',
        version='0.1',
        description='AWS API Gateway Lambda Authorizer',
        url='https://github.com/Ch3ck/api-gateway-authorizer-lambda',
        author='Nyah Check',
        author_email='check.nyah@gmail.com',
        
        install_requires=[reqs],
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False
    )