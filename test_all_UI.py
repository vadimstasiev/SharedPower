from __init__ import uiInterface
# This doesn't work very well, need to find a better solution, TODO
instance1 = uiInterface()
instance1.log_in_ui()
instance2 = uiInterface()
instance2.register_user_ui()
instance3 = uiInterface()
instance3.register_tool_ui()
instance4 = uiInterface()
instance4.tool_owner_options_ui()
instance5 = uiInterface()
instance5.tool_user_options_ui()

# this wont work either btw the root gets destroyed when the application quits
test_intance = uiInterface()
test_intance.log_in_ui()
test_intance.register_user_ui()
test_intance.register_tool_ui()
test_intance.tool_owner_options_ui()
test_intance.tool_user_options_ui()
