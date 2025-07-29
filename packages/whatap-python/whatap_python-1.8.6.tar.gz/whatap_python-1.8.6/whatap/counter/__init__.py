from .counter_manager import CounterMgr  # CounterMgr 클래스 import

# CounterMgr 인스턴스를 생성하고 시작하도록 설정
mgr = CounterMgr()
mgr.setDaemon(True)
mgr.start()
