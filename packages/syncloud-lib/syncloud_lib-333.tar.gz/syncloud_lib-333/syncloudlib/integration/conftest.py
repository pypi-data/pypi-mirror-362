import pytest
import os
from os.path import join, exists
from selenium import webdriver

from syncloudlib.integration.installer import get_data_dir, get_app_dir, get_service_prefix, get_ssh_env_vars, get_snap_data_dir
from syncloudlib.integration.device import Device
from syncloudlib.integration.selenium_wrapper import SeleniumWrapper


def pytest_addoption(parser):
    parser.addoption("--domain", action="store", default="device.com")
    parser.addoption("--device-host", action="store")
    parser.addoption("--app-archive-path", action="store")
    parser.addoption("--app", action="store")
    parser.addoption("--ui-mode", action="store", default="desktop")
    parser.addoption("--device-user", action="store", default="user")
    parser.addoption("--build-number", action="store", default="local")
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--browser-height", action="store", default=1000)
    parser.addoption("--redirect-user", action="store", default="redirect-user-notset")
    parser.addoption("--redirect-password", action="store", default="redirect-password-notset")
    parser.addoption("--distro", action="store", default="distro")
    parser.addoption("--arch", action="store", default="unset-arch")


@pytest.fixture(scope='session')
def build_number(request):
    return request.config.getoption("--build-number")
    

@pytest.fixture(scope='session')
def device_user(request):
    return request.config.getoption("--device-user")
    
    
@pytest.fixture(scope='session')
def device_password():
    return 'Password1'
    

@pytest.fixture(scope='session')
def redirect_user(request):
    return request.config.getoption("--redirect-user")


@pytest.fixture(scope='session')
def redirect_password(request):
    return request.config.getoption("--redirect-password")
    
    
@pytest.fixture(scope='session')
def app(request):
    return request.config.getoption("--app")


@pytest.fixture(scope='session')
def ui_mode(request):
    return request.config.getoption("--ui-mode")


@pytest.fixture(scope='session')
def app_archive_path(request):
    return request.config.getoption("--app-archive-path")


@pytest.fixture(scope='session')
def device_host(request, app, domain):
    device_host = request.config.getoption("--device-host")
    if device_host:
        return device_host
    return '{0}.{1}'.format(app, domain)


@pytest.fixture(scope='session')
def domain(request, distro):
    domain = request.config.getoption("--domain")
    if domain:
        return domain
    return '{0}.com'.format(distro)


@pytest.fixture(scope='session')
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope='session')
def browser_height(request):
    return int(request.config.getoption("--browser-height"))


@pytest.fixture(scope='session')
def distro(request):
    return request.config.getoption("--distro")


@pytest.fixture(scope='session')
def arch(request):
    return request.config.getoption("--arch")


@pytest.fixture(scope='session')
def app_domain(app, domain):
    return '{0}.{1}'.format(app, domain)
    

@pytest.fixture(scope="session")
def platform_data_dir():
    return get_data_dir('platform')

    
@pytest.fixture(scope="session")
def data_dir(app):
    return get_data_dir(app)


@pytest.fixture(scope="session")
def snap_data_dir(app):
    return get_snap_data_dir(app)


@pytest.fixture(scope="session")
def app_dir(app):
    return get_app_dir(app)
    

@pytest.fixture(scope="session")
def service_prefix():
    return get_service_prefix()


def new_firefox_driver(hub_url, ui_mode):
    #desktop_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/100.0"
    mobile_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1"
        
    options = webdriver.FirefoxOptions()
    options.set_preference('app.update.auto', False)
    options.set_preference('app.update.enabled', False)
    if ui_mode == "mobile":
        options.set_preference("general.useragent.override", mobile_agent)
    options.set_preference("devtools.console.stdout.content", True)
    options.set_capability('acceptInsecureCerts', True)
    options.set_capability('se:recordVideo', True)
    options.set_preference("media.navigator.streams.fake", True)
    options.set_preference("media.navigator.permission.disabled", True)

    return webdriver.Remote(
        command_executor=hub_url,
        options=options
    )


def new_chrome_driver(hub_url, ui_mode):
    #desktop_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/100.0"
    mobile_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1"
 
    options = webdriver.ChromeOptions()
    if ui_mode == "mobile":
        options.add_argument('user-agent={}'.format(mobile_agent))
    #options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    options.set_capability('acceptInsecureCerts', True)
    options.set_capability('se:recordVideo', True)
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--use-fake-device-for-media-stream")
    return webdriver.Remote(
        command_executor=hub_url,
        options=options
    )


@pytest.fixture(scope="session")
def driver(ui_mode, browser, browser_height, request):
    hub_url = 'http://selenium:4444/wd/hub'
    width = 1024
    if ui_mode == "mobile":
        width = 400

    if browser == "firefox":
        driver = new_firefox_driver(hub_url, ui_mode)
    else:
        driver = new_chrome_driver(hub_url, ui_mode)
    driver.set_window_rect(0, 0, width, browser_height)

    def driver_quit():
        driver.quit()

    request.addfinalizer(driver_quit)

    return driver


@pytest.fixture(scope="session")
def ssh_env_vars(app):
    return get_ssh_env_vars(app)


@pytest.fixture(scope='function')
def device_session(device):
    return device.login()


@pytest.fixture(scope="session")
def device(domain, device_user,
           device_password, redirect_user, redirect_password, ssh_env_vars):
    return Device(domain, device_user,
                  device_password, redirect_user, redirect_password, ssh_env_vars)


@pytest.fixture(scope="session")
def log_dir(project_dir):
    dir = join(project_dir, 'log')
    if not exists(dir):
        os.mkdir(dir)
    return dir


@pytest.fixture(scope="session")
def artifact_dir(project_dir, distro):
    dir = join(project_dir, 'artifact', distro)
    if not exists(dir):
        os.mkdir(dir)
    return dir


@pytest.fixture(scope="session")
def screenshot_dir(artifact_dir, ui_mode):
    ui_dir = join(artifact_dir, ui_mode)
    if not exists(ui_dir):
        os.mkdir(ui_dir)
    dir = join(ui_dir, 'screenshot')
    if not exists(dir):
        os.mkdir(dir)
    return dir


@pytest.fixture(scope="session")
def selenium_timeout():
    return 30


@pytest.fixture(scope="session")
def selenium(driver, ui_mode, screenshot_dir, app_domain, selenium_timeout, browser):
    return SeleniumWrapper(driver, ui_mode, screenshot_dir, app_domain, selenium_timeout, browser)
