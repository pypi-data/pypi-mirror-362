import os
import sys
from pathlib import Path
from typing import Literal, Optional, List, Tuple

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    MoveTargetOutOfBoundsException,
    InvalidSelectorException,
    SessionNotCreatedException,
    WebDriverException
)


class WebDriverFactory:
    """
    Gerencia a criação e o ciclo de vida de uma única instância do WebDriver.
    Implementa o padrão Singleton para garantir um único driver em toda a aplicação.
    """
    _instance = None
    _logger = None

    @staticmethod
    def get_driver(headless=False, proxy_config=None, selenium_wire=False):
        """
        Retorna a instância do WebDriver. Se não existir, a cria.
        
        Args:
            headless (bool): Se o navegador deve ser iniciado em modo headless.
            proxy_config (dict): Configurações de proxy para o driver.
            selenium_wire (bool): Se deve usar selenium-wire.
            
        Returns:
            WebDriver: A instância do WebDriver.
        """
        if WebDriverFactory._instance and WebDriverFactory._is_driver_alive():
            return WebDriverFactory._instance

        WebDriverFactory._create_new_driver(
            headless=headless,
            proxy_config=proxy_config,
            selenium_wire=selenium_wire
        )
        return WebDriverFactory._instance

    @staticmethod
    def _is_driver_alive():
        """
        Verifica se a instância do driver está viva.
        
        Returns:
            bool: True se o driver estiver ativo, False caso contrário.
        """
        try:
            # Tenta executar uma operação simples para verificar o estado do driver
            WebDriverFactory._instance.current_url
            return True
        except (WebDriverException, AttributeError):
            return False

    @staticmethod
    def _create_new_driver(headless, proxy_config, selenium_wire):
        """
        Cria uma nova instância do WebDriver com as configurações fornecidas.
        """
        options = WebDriverFactory._get_chrome_options(headless)
        service = WebDriverFactory._get_service_path()
        wire_options = WebDriverFactory._get_selenium_wire_options(proxy_config)

        try:
            if selenium_wire:
                from seleniumwire import webdriver as seleniumwiredriver
                WebDriverFactory._instance = seleniumwiredriver.Chrome(
                    service=service,
                    options=options,
                    seleniumwire_options=wire_options
                )
            else:
                WebDriverFactory._instance = webdriver.Chrome(
                    service=service,
                    options=options
                )

            WebDriverFactory._instance.maximize_window()
        except Exception as e:
            WebDriverFactory.quit_driver()
            raise SessionNotCreatedException(
                f"Falha ao iniciar o WebDriver. Verifique a instalação e o PATH. Detalhes: {e}"
            )

    @staticmethod
    def _get_chrome_options(headless):
        """Configura e retorna as opções do Chrome."""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        # Exemplo de boa prática:
        # Adicionar o argumento abaixo para evitar logs desnecessários.
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-logging"]
        )
        return chrome_options

    @staticmethod
    def _get_selenium_wire_options(proxy_config):
        """Configura e retorna as opções do Selenium-Wire."""
        if not proxy_config:
            return {}
        return {
            'proxy': proxy_config,
            'suppress_connection_errors': False,
        }

    @staticmethod
    def _get_service_path():
        """Obtém o Service para o ChromeDriver, tentando o gerenciador e depois o caminho local."""
        try:
            return Service(executable_path=ChromeDriverManager().install())
        except Exception:
            # Fallback para um caminho local
            # Considerar usar variáveis de ambiente para caminhos.
            local_path = Path.home() / "Downloads/Chromedriver.exe"
            if not local_path.exists():
                raise FileNotFoundError(
                    f"ChromeDriver não encontrado em {local_path}. "
                    "Tente instalar via `webdriver-manager` ou coloque-o no caminho especificado."
                )
            return Service(executable_path=local_path)

    @staticmethod
    def quit_driver():
        """Encerra a instância do driver e a define como None."""
        if WebDriverFactory._instance:
            try:
                WebDriverFactory._instance.quit()
                WebDriverFactory._logger.info("Driver encerrado com sucesso.")
            except Exception as e:
                WebDriverFactory._logger.error(f"Erro ao encerrar o driver: {e}")
            finally:
                WebDriverFactory._instance = None

    @staticmethod
    def restart_driver(headless=False, proxy_config=None, selenium_wire=False):
        """Reinicia o driver, encerrando a instância atual e criando uma nova."""
        WebDriverFactory._logger.info("Reiniciando o driver.")
        WebDriverFactory.quit_driver()
        return WebDriverFactory.get_driver(
            headless=headless,
            proxy_config=proxy_config,
            selenium_wire=selenium_wire
        )


class ActionsSelenium:
    def __init__(self, driver: WebDriver, logger):
        if not isinstance(driver, WebDriver):
            raise TypeError("A instância do driver deve ser um objeto WebDriver.")
        self.driver = driver
        self.action_chains = ActionChains(self.driver)
        self.logger = logger

    def _select_element_type(self, element_type: str):
        selector_map = {
            'id': By.ID,
            'name': By.NAME,
            'class': By.CLASS_NAME,
            'xpath': By.XPATH,
            'tag_name': By.TAG_NAME,
            'css_selector': By.CSS_SELECTOR,
        }
        if element_type.lower() not in selector_map:
            raise ValueError(f"Seletor '{element_type}' não suportado.")
        return selector_map[element_type.lower()]

    def _find_element(
        self,
        name: str,
        silence: bool = False,
        timeout: int = 60,
        selector: str = 'xpath',
    ) -> Optional[WebElement]:
        try:
            element_type = self._select_element_type(selector)
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(
                EC.presence_of_element_located((element_type, name))
            )
            return element
        except TimeoutException:
            if not silence:
                self.logger.error(f"Elemento não encontrado no tempo limite: {name}")
        except (NoSuchElementException, InvalidSelectorException) as e:
            if not silence:
                self.logger.error(f"Elemento não encontrado ou seletor inválido: {name} - Detalhes: {e}")
        except Exception as e:
            if not silence:
                self.logger.error(f"Erro inesperado ao buscar elemento: {e}")
        return None

    def _search_recursively_in_frames(
        self, selector: str, name: str, frame: Optional[WebElement] = None
    ) -> Optional[WebElement]:
        """Busca um elemento em todos os frames de forma recursiva."""
        try:
            self.driver.switch_to.frame(frame)
        except Exception:
            return None

        # Tenta encontrar o elemento no frame atual
        try:
            element = self.driver.find_element(self._select_element_type(selector), name)
            return element
        except NoSuchElementException:
            pass
        
        # Encontra e busca em frames aninhados
        frames_in_current_context = self.driver.find_elements(By.TAG_NAME, "iframe") + self.driver.find_elements(By.TAG_NAME, "frame")
        for child_frame in frames_in_current_context:
            result = self._search_recursively_in_frames(selector, name, child_frame)
            if result:
                return result
        
        # Volta para o frame pai se a busca falhar
        try:
            self.driver.switch_to.parent_frame()
        except Exception:
            pass
        
        return None

    def find_element_in_frames(
        self,
        name: str,
        selector: str = 'xpath',
        silence: bool = False
    ) -> Optional[WebElement]:
        """Busca um elemento em todos os frames da página, incluindo aninhados."""
        self.driver.switch_to.default_content()
        element = self._search_recursively_in_frames(selector, name)

        if not element and not silence:
            self.logger.error(f"Elemento '{name}' não encontrado em nenhum frame.")
        
        return element

    # Métodos de Ação (Refatoração de 'interact_with_frame_element')
    def click_element_in_frames(self, name: str, selector: str = 'xpath', **kwargs):
        """Busca e clica em um elemento em frames."""
        element = self.find_element_in_frames(name, selector, kwargs.get('silence', False))
        if element:
            self._safe_click(element)
            return True
        self._handle_interaction_error(name, kwargs.get('silence', False))

    def get_text_from_element_in_frames(self, name: str, selector: str = 'xpath', **kwargs) -> Optional[str]:
        """Busca e retorna o texto de um elemento em frames."""
        element = self.find_element_in_frames(name, selector, kwargs.get('silence', False))
        if element:
            return element.text
        self._handle_interaction_error(name, kwargs.get('silence', False))

    def send_keys_to_element_in_frames(self, name: str, keys: str, selector: str = 'xpath', **kwargs):
        """Busca um elemento em frames e envia chaves."""
        element = self.find_element_in_frames(name, selector, kwargs.get('silence', False))
        if element:
            element.send_keys(keys)
            return True
        self._handle_interaction_error(name, kwargs.get('silence', False))

    def _safe_click(self, element: WebElement):
        """Tenta clicar no elemento, lidando com exceções de visibilidade."""
        try:
            element.click()
        except MoveTargetOutOfBoundsException as e:
            self.logger.error(f"Elemento fora da visibilidade: {e}")
            raise

    def double_click_and_send_keys(self, element: WebElement, clean: bool = False, keys: Optional[str] = None):
        """
        Executa um clique duplo, limpa o campo se solicitado e envia novas chaves.
        
        Args:
            element (WebElement): O elemento para interagir.
            clean (bool): Se deve limpar o campo antes de enviar as chaves.
            keys (Optional[str]): As chaves a serem enviadas.
        """
        try:
            self.action_chains.double_click(element).perform()
            if clean:
                element.send_keys(Keys.DELETE)
            if keys:
                element.send_keys(keys)
        except MoveTargetOutOfBoundsException as e:
            self.logger.error(f"Elemento fora da visibilidade: {e}")
            raise

    def _handle_interaction_error(self, name: str, silence: bool):
        """
        Lida com erros de interação e levanta exceções se não estiver em modo silencioso.
        """
        message = f"Elemento '{name}' não encontrado para interação."
        if not silence:
            self.logger.error(message)
        raise NoSuchElementException(message)

    def page_refresh(self):
        """Atualiza a página."""
        self.driver.refresh()

    def change_tab(self, tab_index: int):
        """Muda para a aba especificada."""
        try:
            self.driver.switch_to.window(self.driver.window_handles[tab_index])
        except IndexError:
            self.logger.error(f"Aba com índice {tab_index} não existe.")
            raise

    # Lógica de negócio específica
    def try_click_advance_button(self, button_id: str, selector: str = 'xpath', max_attempts: int = 3):
        """
        Método específico para clicar em um botão de avançar, buscando em frames.
        """
        found_elements = []
        visited_frames = set()

        def search(frame: Optional[WebElement] = None):
            nonlocal found_elements
            # Se o frame já foi visitado, evita loop infinito
            if frame and id(frame) in visited_frames:
                return
            if frame:
                visited_frames.add(id(frame))

            try:
                self.driver.switch_to.frame(frame)
                element = self._find_element(button_id, selector=selector, timeout=1, silence=True)
                if element:
                    found_elements.append(element)
            except Exception as e:
                self.logger.debug(f"Erro ao mudar para frame ou encontrar elemento: {e}")

            # Busca recursiva em sub-frames
            frames_in_current_context = self.driver.find_elements(By.TAG_NAME, "iframe") + self.driver.find_elements(By.TAG_NAME, "frame")
            for child_frame in frames_in_current_context:
                search(child_frame)

            # Volta ao frame pai
            try:
                self.driver.switch_to.parent_frame()
            except Exception:
                pass

        self.driver.switch_to.default_content()
        search(frame=None)

        if not found_elements:
            self.logger.error('Nenhum botão de avançar encontrado.')
            raise NoSuchElementException('Botão para avançar etapa não localizado.')

        for attempt in range(max_attempts):
            for element in found_elements:
                try:
                    self._safe_click(element)
                    return True
                except Exception:
                    self.logger.warning(f"Tentativa {attempt + 1}: Erro ao clicar no botão. Tentando novamente...")
                    continue
        
        self.logger.error(f"Falha ao clicar no botão após {max_attempts} tentativas.")
        raise MoveTargetOutOfBoundsException("Botão para avançar etapa inacessível ou fora da tela.")


class SetupDriverSelenium:
    @staticmethod
    def make(
        logger,
        headless: bool = False,
        proxy_config: dict = None,
        selenium_wire: bool = False,
    ) -> Tuple[WebDriver, 'ActionsSelenium']:
        """
        Configura o ambiente de automação, instanciando o WebDriver e a
        classe de ações.

        Args:
            headless (bool): Se o navegador deve ser iniciado em modo headless.
            proxy_config (dict): Configurações de proxy.
            selenium_wire (bool): Se deve usar selenium-wire.

        Returns:
            (WebDriver, ActionsSelenium): Instância do WebDriver e a Instância de ActionsSelenium.
        """
        # 1. Configurar o logger na classe de fábrica
        # Esta é uma dependência que a fábrica precisa para funcionar corretamente.
        WebDriverFactory._logger = logger
        
        # 2. Obter ou criar a instância do WebDriver usando a fábrica
        driver = WebDriverFactory.get_driver(
            headless=headless,
            proxy_config=proxy_config,
            selenium_wire=selenium_wire
        )

        # 3. Validar se o driver foi criado com sucesso
        if driver is None:
            raise RuntimeError("Falha ao obter a instância do WebDriver.")

        # 4. Instanciar a classe de ações com o driver e o logger
        actions = ActionsSelenium(driver, logger)

        # 5. Retornar as instâncias
        return driver, actions


if __name__ == '__main__':
    driver, act = SetupDriverSelenium.make(None)

    driver.get("https://www.google.com/")
    search = act._find_element('//*[@title="Pesquisar"]')
    search.send_keys(":)", Keys.ENTER)
    ...