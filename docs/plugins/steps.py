"""
An autodocumenter for Aloe steps

FIXME: move this to Aloe
"""

from types import FunctionType

from sphinx.ext.autodoc import FunctionDocumenter, ModuleDocumenter
from sphinx.util.inspect import safe_getmembers


def is_step(member):
    return isinstance(member, FunctionType) and hasattr(member, 'sentence')


class StepsDocumenter(ModuleDocumenter):
    def get_object_members(self, want_all):
        ret, memberlist = super().get_object_members(want_all)

        # override __all__ find the steps also
        for name, member in safe_getmembers(self.object):
            if is_step(member):
                if (name, member) in memberlist:
                    continue

                memberlist.append((name, member))

        return ret, memberlist

    def filter_members(self, members, want_all):
        members_copy = list(members)

        members = super().filter_members(members, want_all)

        # add back in the steps, even if private
        for (name, member) in members_copy:
            if is_step(member):
                if (name, member, False) in members:
                    continue

                members.append((name, member, False))

        return members


class StepDocumenter(FunctionDocumenter):

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        return is_step(member) or \
            super().can_document_member(member, membername, isattr, parent)

    def add_directive_header(self, sig):
        if is_step(self.object):
            # FIXME: this is a first cut
            directive = 'describe'
            name = self.object.sentence
            sourcename = self.get_sourcename()

            self.add_line(u'.. %s:: %s' % (directive, name),
                          sourcename)
            if self.options.noindex:
                self.add_line(u'   :noindex:', sourcename)
        else:
            return super().add_directive_header(sig)


def setup(app):
    app.add_autodocumenter(StepsDocumenter)
    app.add_autodocumenter(StepDocumenter)

    return {'version': '0.1', 'parallel_read_safe': False}
