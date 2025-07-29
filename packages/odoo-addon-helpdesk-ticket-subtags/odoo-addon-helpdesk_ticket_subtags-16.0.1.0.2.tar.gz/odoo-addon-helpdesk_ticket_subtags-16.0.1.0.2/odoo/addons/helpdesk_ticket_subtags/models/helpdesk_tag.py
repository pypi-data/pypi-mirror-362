from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HelpdeskTag(models.Model):
    _inherit = "helpdesk.ticket.tag"
    _description = "Helpdesk Tags and Subtags"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "display_name"
    _order = "display_name"

    name = fields.Char("Name", required=True)
    display_name = fields.Char(
        "Complete Name", compute="_compute_display_name", store=True, recursive=True
    )
    parent_id = fields.Many2one(
        "helpdesk.ticket.tag", string="Main Tag", index=True, ondelete="cascade"
    )
    parent_path = fields.Char(index=True, unaccent=False)
    child_id = fields.One2many("helpdesk.ticket.tag", "parent_id", string="Subtags")

    @api.constrains("parent_id")
    def _check_circular_reference(self):
        for record in self:
            tag = record.parent_id
            while tag:
                if tag == record:
                    raise ValidationError(
                        _("Circular reference detected for tag '%s'." % record.name)
                    )
                tag = tag.parent_id

    @api.depends("name", "parent_id.display_name")
    def _compute_display_name(self):
        for record in self:
            if record.parent_id:
                record.display_name = "%s / %s" % (
                    record.parent_id.display_name,
                    record.name,
                )
            else:
                record.display_name = record.name

    def _get_record_parents(self, field):
        if not self.parent_id:
            return []
        return self.parent_id._get_record_parents(field) + [
            (self.id, str(getattr(self, field)))
        ]

    def _get_record_direct_childs(self, field, domain):
        if not self.id:
            return [
                (r.id, str(getattr(r, field)))
                for r in self.search([("parent_id", "=", False)])
            ]
        return [
            (r.id, str(getattr(r, field)))
            for r in self.search([("parent_id", "=", self.id)] + domain)
        ]

    def get_record_direct_childs_parents(self, domain=False):
        if not domain:
            domain = []
        field = "name"
        return {
            "childs": self._get_record_direct_childs(field, domain),
            "parents": self._get_record_parents(field),
        }

    def name_get(self):
        result = []
        for tag in self:
            result.append((tag.id, tag.display_name))
        return result
