# 
import frappe
from frappe import _
from frappe.model.workflow import (
	get_workflow_name,
	get_workflow_state_field
)
from frappe.workflow.doctype.workflow_action.workflow_action import get_doc_workflow_state
from frappe.utils import now,format_duration, get_datetime
from datetime import datetime

def get_workflow_field_value(workflow_name, field):
	value = frappe.cache().hget("workflow_" + workflow_name, field)
	if value is None:
		value = frappe.db.get_value("Workflow", workflow_name, field)
		frappe.cache().hset("workflow_" + workflow_name, field, value)
	return value

def get_workflow_tracing_table_field(workflow_name):
	tracing_table_field = get_workflow_field_value(workflow_name, "tracing_table_field")
	if tracing_table_field:
		return tracing_table_field

def update_tracing_table(doc, method=None):
    # frappe.clear_cache(doctype = doc.document_type)

    workflow_name = get_workflow_name(doc.get("doctype"))
    # workflow = frappe.get_doc("Workflow", workflow_name)
    if not workflow_name:
        return
    tracing_table_field = get_workflow_tracing_table_field(workflow_name)
	
    if tracing_table_field:
					doc_before_save = doc.get_doc_before_save()
					if doc_before_save:
						rows = len(doc.get(tracing_table_field)) 
						last_state = get_doc_workflow_state(doc_before_save)
						if rows == 1:
							last_state_time = doc.get(tracing_table_field)[0].date
							current_state_time = now()
						else:
							last_state_time = doc.get(tracing_table_field)[rows - 1].date
							current_state_time = now()

					else:
						last_state = ""
						last_state_time = now()
						current_state_time = now()

					current_state =  get_doc_workflow_state(doc)
					duration_in_seconds = cal_duration(last_state_time,current_state_time)
					duration_in_seconds_str = duration_in_seconds
					user = frappe.session.user
					user_name = frappe.db.get_value("User", user, 'full_name')
					employee  = frappe.db.get_value("Employee", {"user_id": user})
					if employee:
						employee_name = frappe.db.get_value("Employee",  employee , "employee_name")

					# frappe.msgprint(_("X = {0} ").format(format_duration(duration_in_seconds)))
					
					if last_state != current_state :
						doc.append(tracing_table_field, {
							'workflow_state': current_state,
							'user':frappe.session.user,
							'user_name': user_name,
							'employee': employee if employee else "",
							'employee_name' : employee_name if employee else "",
							'date': now() ,
							'duration_in_seconds': duration_in_seconds,
							'duration': duration_in_seconds_str
						})
					
					# frappe.msgprint(_("X = {0} ").format(duration_in_seconds))
					
		
    
    
frappe.whitelist()
def cal_duration(start,end):
	s = get_datetime(start)
	e = get_datetime(end)
	seconds = (e.second +e.minute*60 + e.hour*3600) - (s.second +s.minute*60 + s.hour*3600)
	if seconds:
		return seconds
	else: 
		return 0