# -*- coding: utf-8 -*-
"""Classes that define flask front end web form."""
from flask_wtf import FlaskForm
from wtforms.validators import Email, Length, DataRequired, InputRequired
from wtforms.fields import (
    DateField,
    FileField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    IntegerField,
    EmailField,
    TextAreaField,
)


class ContactForm(FlaskForm):
    """Class to generate html code which contain contact form."""

    solution = StringField(
        "Solution name",
        validators=[
            InputRequired(),
            DataRequired(),
            Length(min=5, max=40, message="Solution name must be between 5 and 40 characters long."),
        ],
        description="The name of the solution or application. Required",
    )

    scope = SelectField(
        "Scope",
        choices=[
            "SAP",
            "Non-SAP",
        ],
        default="Non-SAP",
        validators=[DataRequired()],
    )

    description = TextAreaField(
        "Description",
        validators=[
            DataRequired(),
            InputRequired(),
            Length(min=200, max=400, message="Description must be between 200 and 400 characters"),
        ],
        description="Description about solution (what is for)",
        render_kw={"rows": 4},
    )

    environment = SelectMultipleField(
        "Environment", choices=["LAB", "NON-PROD (dev/test/stage)", "PROD"], validators=[DataRequired()]
    )

    bu_owner = EmailField("Business Owner", validators=[Email(), DataRequired(), InputRequired()], description="Email")

    it_owner = EmailField("IT Owner", validators=[Email(), DataRequired(), InputRequired()], description="Email")

    cost_center = StringField(
        "Cost Center",
        validators=[
            DataRequired(),
            InputRequired(),
        ],
        description="CostCenter ID",
    )

    cats_network_id = IntegerField(
        "CATS network ID",
        validators=[
            DataRequired(),
            InputRequired(),
        ],
    )

    priority = SelectField(
        "Priority",
        choices=["Highest", "High", "Medium", "Low", "Lowest"],
        validators=[DataRequired()],
        default="Medium",
    )

    proposed_start_date = DateField(
        "Proposed Start Date", validators=[InputRequired()], description="Start of the project"
    )

    proposed_due_date = DateField(
        "Proposed Due Date", validators=[InputRequired()], description="Estimated time of delivery"
    )
    epic_link = StringField("Epic link", validators=[DataRequired()], description="Epic link", default="TCA-3927")

    attachment = FileField("Attachments (optional)", description="6MB limit")

    submit_button = SubmitField("Send message")
