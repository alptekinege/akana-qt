"""Akana Qt — labeled field composition (web `.ak-field`).

Label (mono) + control + optional helper / error. Error state uses ink border
on the control via dynamic property `akError` (no red accent).
"""

from __future__ import annotations

from PyQt6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget

from akana.tokens import SPACE
from akana.util import AkFlowLabel, set_dyn


class AkField(QWidget):
    """Vertical stack: label → control → helper."""

    def __init__(
        self,
        label: str = "",
        control: QWidget | None = None,
        *,
        helper: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("AkField")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(SPACE[2])

        self._label = QLabel(label)
        self._label.setObjectName("akFieldLabel")
        self._label.setVisible(bool(label))
        root.addWidget(self._label)

        self._control = control
        if control is not None:
            control.setSizePolicy(
                QSizePolicy.Policy.Expanding, control.sizePolicy().verticalPolicy()
            )
            root.addWidget(control)

        self._helper = AkFlowLabel(helper, object_name="akHelper")
        self._helper.setVisible(bool(helper))
        root.addWidget(self._helper)

        self._error = False

    def control(self) -> QWidget | None:
        return self._control

    def set_label(self, text: str) -> None:
        self._label.setText(text)
        self._label.setVisible(bool(text))

    def set_helper(self, text: str) -> None:
        self._helper.setText(text)
        self._helper.setVisible(bool(text))
        if not self._error:
            self._helper.setObjectName("akHelper")
            from akana.util import repolish

            repolish(self._helper)

    def set_error(self, message: str | None = None) -> None:
        """Mark field invalid. Border via `akError` on control; helper uses body text color."""
        self._error = True
        if self._control is not None:
            set_dyn(self._control, "akError", True)
        if message is not None:
            self._helper.setText(message)
            self._helper.setVisible(bool(message))
        self._helper.setObjectName("akHelperError")
        from akana.util import repolish

        repolish(self._helper)

    def clear_error(self) -> None:
        self._error = False
        if self._control is not None:
            set_dyn(self._control, "akError", False)
        self._helper.setObjectName("akHelper")
        from akana.util import repolish

        repolish(self._helper)
