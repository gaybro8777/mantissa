from setuptools import setup, find_packages
import versioneer

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    name="Mantissa",
    maintainer="Tristan Seligmann",
    maintainer_email="mithrandi@mithrandi.net",
    url="https://github.com/twisted/mantissa",
    license="MIT",
    platforms=["any"],
    description="A multiprotocol application deployment platform",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: No Input/Output (Daemon)",
        "Framework :: Twisted",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Terminals",
        ],
    install_requires=[
        "Twisted>=16.0.0",
        "PyOpenSSL>=0.13",
        "Axiom>=0.7.0",
        "Vertex>=0.2.0",
        "PyTZ",
        "Pillow",
        "cssutils>=0.9.5",
        "Nevow>=0.9.5",
        ],
    packages=find_packages() + ['axiom.plugins', 'nevow.plugins'],
    include_package_data=True,
    )
