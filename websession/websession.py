from playwright.sync_api import sync_playwright

class WebSession:
  def __init__(
      self,
      playwright: any,
      record_video: bool = False,
  ):
    self.browser = playwright.chromium.launch()

    if record_video:
      self.context = self.browser.new_context(
        record_video_dir="./output/",
        )
    else:
      self.context = self.browser.new_context()

    self.page = self.context.new_page()

  # Destructor __del__ does not work well
  # def __del__(self):
  def close(self):
    self.context.close()
    self.browser.close()
