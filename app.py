import webview
import config as cfg
import backend.api as api
import logging

if cfg.get("logging.enabled", False):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(cfg.get("logging.log_file", "ledgerly.log"), mode="w"),   # file
            logging.StreamHandler()           # terminal
        ],
    )


app_api = api.LedgerlyApi()

if __name__ == '__main__':
    first_window = webview.create_window(cfg.get("window.title", "Ledgerly"), cfg.get("window.frontend"), min_size=(int(cfg.get("window.min_width", "740")), int(cfg.get("window.min_height", "200"))), js_api=app_api)
    webview.start(args=first_window, debug=cfg.get("dev_mode", False))
