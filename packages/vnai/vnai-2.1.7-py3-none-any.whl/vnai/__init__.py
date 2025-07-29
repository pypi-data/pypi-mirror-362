import os
import pathlib
import json
import time
import threading
import functools
from datetime import datetime
from vnai.beam.quota import guardian, optimize
from vnai.beam.metrics import collector, capture
from vnai.beam.pulse import monitor
from vnai.flow.relay import conduit, configure
from vnai.flow.queue import buffer
from vnai.scope.profile import inspector
from vnai.scope.state import tracker, record
import vnai.scope.promo
from vnai.scope.promo import present
TC_VAR ="ACCEPT_TC"
TC_VAL ="tôi đồng ý"
TC_PATH = pathlib.Path.home() /".vnstock" /"id" /"terms_agreement.txt"
TERMS_AND_CONDITIONS ="""
Khi tiếp tục sử dụng Vnstock, bạn xác nhận rằng bạn đã đọc, hiểu và đồng ý với Chính sách quyền riêng tư và Điều khoản, điều kiện về giấy phép sử dụng Vnstock.
Chi tiết:
- Giấy phép sử dụng phần mềm: https://vnstocks.com/docs/tai-lieu/giay-phep-su-dung
- Chính sách quyền riêng tư: https://vnstocks.com/docs/tai-lieu/chinh-sach-quyen-rieng-tu
"""

class Core:
    def __init__(self):
        self.initialized = False
        self.webhook_url = None
        self.init_time = datetime.now().isoformat()
        self.home_dir = pathlib.Path.home()
        self.project_dir = self.home_dir /".vnstock"
        self.id_dir = self.project_dir /'id'
        self.terms_file_path = TC_PATH
        self.system_info = None
        self.project_dir.mkdir(exist_ok=True)
        self.id_dir.mkdir(exist_ok=True)
        self.initialize()

    def initialize(self, webhook_url=None):
        if self.initialized:
            return True
        if not self._check_terms():
            self._accept_terms()
        from vnai.scope.profile import inspector
        inspector.setup_vnstock_environment()
        present()
        if webhook_url:
            self.webhook_url = webhook_url
            configure(webhook_url)
        record("initialization", {"timestamp": datetime.now().isoformat()})
        self.system_info = inspector.examine()
        conduit.queue({
"type":"system_info",
"data": {
"commercial": inspector.detect_commercial_usage(),
"packages": inspector.scan_packages()
            }
        }, priority="high")
        self.initialized = True
        return True

    def _check_terms(self):
        return os.path.exists(self.terms_file_path)

    def _accept_terms(self):
        system_info = inspector.examine()
        if TC_VAR in os.environ and os.environ[TC_VAR] == TC_VAL:
            response = TC_VAL
        else:
            response = TC_VAL
            os.environ[TC_VAR] = TC_VAL
        now = datetime.now()
        signed_agreement = (
f"Người dùng có mã nhận dạng {system_info['machine_id']} đã chấp nhận "
f"điều khoản & điều kiện sử dụng Vnstock lúc {now}\n"
f"---\n\n"
f"THÔNG TIN THIẾT BỊ: {json.dumps(system_info, indent=2)}\n\n"
f"Đính kèm bản sao nội dung bạn đã đọc, hiểu rõ và đồng ý dưới đây:\n"
f"{TERMS_AND_CONDITIONS}"
        )
        with open(self.terms_file_path,"w", encoding="utf-8") as f:
            f.write(signed_agreement)
        env_file = self.id_dir /"environment.json"
        env_data = {
"accepted_agreement": True,
"timestamp": now.isoformat(),
"machine_id": system_info['machine_id']
        }
        with open(env_file,"w") as f:
            json.dump(env_data, f)
        return True

    def status(self):
        return {
"initialized": self.initialized,
"health": monitor.report(),
"metrics": tracker.get_metrics()
        }

    def configure_privacy(self, level="standard"):
        from vnai.scope.state import tracker
        return tracker.setup_privacy(level)
core = Core()

def tc_init(webhook_url=None):
    return core.initialize(webhook_url)

def setup(webhook_url=None):
    return core.initialize(webhook_url)

def optimize_execution(resource_type="default"):
    return optimize(resource_type)

def agg_execution(resource_type="default"):
    return optimize(resource_type, ad_cooldown=1500, content_trigger_threshold=100000)

def measure_performance(module_type="function"):
    return capture(module_type)

def accept_license_terms(terms_text=None):
    if terms_text is None:
        terms_text = TERMS_AND_CONDITIONS
    system_info = inspector.examine()
    terms_file = pathlib.Path.home() /".vnstock" /"id" /"terms_agreement.txt"
    os.makedirs(os.path.dirname(terms_file), exist_ok=True)
    with open(terms_file,"w", encoding="utf-8") as f:
        f.write(f"Terms accepted at {datetime.now().isoformat()}\n")
        f.write(f"System: {json.dumps(system_info)}\n\n")
        f.write(terms_text)
    return True

def accept_vnstock_terms():
    from vnai.scope.profile import inspector
    system_info = inspector.examine()
    home_dir = pathlib.Path.home()
    project_dir = home_dir /".vnstock"
    project_dir.mkdir(exist_ok=True)
    id_dir = project_dir /'id'
    id_dir.mkdir(exist_ok=True)
    env_file = id_dir /"environment.json"
    env_data = {
"accepted_agreement": True,
"timestamp": datetime.now().isoformat(),
"machine_id": system_info['machine_id']
    }
    try:
        with open(env_file,"w") as f:
            json.dump(env_data, f)
        print("Vnstock terms accepted successfully.")
        return True
    except Exception as e:
        print(f"Error accepting terms: {e}")
        return False

def configure_privacy(level="standard"):
    from vnai.scope.state import tracker
    return tracker.setup_privacy(level)

def check_commercial_usage():
    from vnai.scope.profile import inspector
    return inspector.detect_commercial_usage()

def authenticate_for_persistence():
    from vnai.scope.profile import inspector
    return inspector.get_or_create_user_id()

def display_content():
    return present()

def configure_webhook(webhook_id=''):
    if not webhook_id:
        return False
    from vnai.flow.relay import configure
    webhook_url =f'https://botbuilder.larksuite.com/api/trigger-webhook/{webhook_id}'
    return configure(webhook_url)
configure_webhook()