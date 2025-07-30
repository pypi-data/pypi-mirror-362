import argparse
from pathlib import Path

from pybenutils.network.download_manager import download_url
from pybenutils.useful import install_pip_package_using_pip


def auto_etp_install(branch):
    """Download and install auto_etp repo package to python site packages"""
    repo_package_url = (f'http://autoetp2.jenkins.akamai.com/job/utils-sources/job/{branch}/lastSuccessfulBuild/'
                        f'artifact/auto_etp.tar.gz')
    if repo_package_url:
        install_pip_package_using_pip(download_url(repo_package_url))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        'Download the auto_etp repo package from our Jenkins server and install using "pip install"')
    parser.add_argument('-b', '--branch', type=str, default='master')
    # parser.add_argument('-n', '--build', type=str, default='lastSuccessfulBuild')
    args = parser.parse_args()

    op = 'http://autoetp2.jenkins.akamai.com/job/utils-online_params/lastSuccessfulBuild/artifact/online_params.py'
    download_url(op, f'{Path.home() / "online_params.py"}')

    auto_etp_install(branch=args.branch)