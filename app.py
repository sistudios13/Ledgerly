import webview
import config as cfg
import backend.api as api
import logging

if cfg.LOGGING_ENABLED:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(cfg.LOG_FILE, mode="w"),   # file
            logging.StreamHandler()           # terminal
        ],
    )


app_api = api.LedgerlyApi()

if __name__ == '__main__':
    first_window = webview.create_window(cfg.WINDOW_TITLE, cfg.WINDOW_FRONTEND, min_size=(cfg.WINDOW_MIN_WIDTH, cfg.WINDOW_MIN_HEIGHT), js_api=app_api)
    webview.start(args=first_window, debug=cfg.DEV_MODE)
