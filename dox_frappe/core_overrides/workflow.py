import frappe
from frappe import _
from frappe.workflow.doctype.workflow.workflow import Workflow

class CustomWorkflow(Workflow):
    def validate(self):
        self.set_active()
        self.create_custom_fields()
        self.update_default_workflow_status()
        self.validate_docstatus()
    
    def create_custom_fields(self):
        
        meta = frappe.get_meta(self.document_type)
        if self.show_tracing_table:
            if not meta.get_field(self.tracing_table_field):
                frappe.get_doc(
                {
                    "doctype": "Custom Field",
                    "dt": self.document_type,
                    "__islocal": 1,
                    "fieldname": self.tracing_table_field,
                    "label": self.tracing_table_field.replace("_", " ").title(),
                    "allow_on_submit": 1,
                    "read_only": 1,
                    "no_copy": 1,
                    "fieldtype": "Table",
                    "options": "Workflow Tracing Details",
                    "owner": "Administrator",
                }
                ).save()

                frappe.msgprint(
                    _("Created Custom Field {0} in {1}").format(self.tracing_table_field, self.document_type)
                )
                frappe.clear_cache(doctype=self.document_type)
        
        if not meta.get_field(self.workflow_state_field):
            frappe.get_doc(
				{
					"doctype": "Custom Field",
					"dt": self.document_type,
					"__islocal": 1,
					"fieldname": self.workflow_state_field,
					"label": self.workflow_state_field.replace("_", " ").title(),
					"hidden": 1,
					"allow_on_submit": 1,
					"no_copy": 1,
					"fieldtype": "Link",
					"options": "Workflow State",
					"owner": "Administrator",
				}
			).save()
            frappe.msgprint(
				_("Created Custom Field {0} in {1}").format(self.workflow_state_field, self.document_type)
			)
            frappe.clear_cache(doctype=self.document_type)

            

    def update_default_workflow_status(self):
        docstatus_map = {}
        states = self.get("states")
        for d in states:
              if not d.doc_status in docstatus_map:
                frappe.db.sql(
					"""
					UPDATE `tab{doctype}`
					SET `{field}` = %s
					WHERE ifnull(`{field}`, '') = ''
					AND `docstatus` = %s
				""".format(
						doctype=self.document_type, field=self.workflow_state_field
					),
					(d.state, d.doc_status),
				)
                docstatus_map[d.doc_status] = d.state

        docstatus_map = {}
        for d in states:
              if not d.doc_status in docstatus_map:
                frappe.db.sql(
					"""
					UPDATE `tab{doctype}`
					SET `{field}` = %s
					WHERE ifnull(`{field}`, '') = ''
					AND `docstatus` = %s
				""".format(
						doctype="Workflow Tracing Details", field= "workflow_state"
					),
					(d.state, d.doc_status),
				)
                docstatus_map[d.doc_status] = d.state

        