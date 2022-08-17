from django import forms

from .models import DiskChanged, DiskFixed, GpuChanged, GpuFixed, NodeChanged, NodeFixed

class NodeFixedForm(forms.ModelForm):
    class Meta:
        model = NodeFixed
        fields = "__all__"


class DiskFixedForm(forms.ModelForm):
    class Meta:
        model = DiskFixed
        fields = "__all__"


class GpuFixedForm(forms.ModelForm):
    class Meta:
        model = GpuFixed
        fields = "__all__"


class NodeChangedForm(forms.ModelForm):
    class Meta:
        model = NodeChanged
        fields = "__all__"


class DiskChangedForm(forms.ModelForm):
    class Meta:
        model = DiskChanged
        fields = "__all__"


class GpuChangedForm(forms.ModelForm):
    class Meta:
        model = GpuChanged
        fields = "__all__"