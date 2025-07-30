from setuptools import setup, find_packages

setup(
    name='hanifx_anti',
    version='10.0.1',
    description='Ultimate Phone Security & Anti-Malware System',
    author='Hanif',
    author_email='sajim4653@gmail.com',
    packages=find_packages(),
    install_requires=[
        'cryptography', 'scapy', 'psutil', 'requests'
    ],
    entry_points={
        'console_scripts': [
            'hanifx-scan=hanifx_anti.core.scanner:start_scan'
        ]
    }
)
