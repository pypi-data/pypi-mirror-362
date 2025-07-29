"""Module defining types for use with Flask-Bauto"""

from dataclasses import dataclass, field, MISSING
from pathlib import Path
import datetime
import os

# Python types
from typing import Annotated, get_args, get_type_hints

## markdown
#type markdown = Annotated[str, {'max_size':255}] # TODO 3.12+ type declaration
markdown = Annotated[str, {'max_size':255}] # TODO 3.12+ type declaration

## url
from urllib.parse import urlparse, ParseResult
url = ParseResult

# Form types
import wtforms as wtf

# DB types
import sqlalchemy as sa
from sqlalchemy.orm import registry, relationship

# Type definitions that also act as descriptors for use on instance instantiation
@dataclass
class BauType:
    py_item: any = None
    db_item: any = None
    ux_item: any = None
    py_type: type = None
    db_type: type = None
    ux_type: type = None
    
    def __post_init__(self):
        if self.py_item is not None:
            if self.db_item is None:
                self.db_item = self.py2db()
            if self.ux_item is None:
                self.ux_item = self.py2ux()
        elif self.db_item is not None:
            if self.py_item is None:
                self.py_item = self.db2py()
            if self.ux_item is None:
                self.ux_item = self.py2ux()
        elif self.ux_item is not None:
            if self.py_item is None:
                self.py_item = self.ux2py()
            if self.db_item is None:
                self.db_item = self.py2db()

    def __call__(self, py_item=None, db_item=None, ux_item=None):
        """Calling the instance of the BauType definition has
        a similar behavior as instantiating the BauType: if an
        item is provided of either py, db, or ux the other types
        are calculated as well. This is achieved by rerunning the
        __post_init__
        """
        if py_item is not None: self.py_item = py_item
        if db_item is not None: self.db_item = db_item
        if ux_item is not None: self.ux_item = ux_item
        self.__post_init__()
        return self
    
    def field(self, *args, **kwargs):
        try:
            kwargs['metadata']['bautype'] = self
        except KeyError: kwargs['metadata'] = {'bautype': self}
        return field(*args, **kwargs)

    # Default transform function names to False to check if transform required
    py2db = False
    py2ux = False
    db2py = False
    ux2py = False

    @classmethod
    def _get_bautypes(cls):
        return {
            t.py_type:t for t in cls.__subclasses__()
        }

    @classmethod
    def _get_bautype(cls, type):
        if hasattr(type,'__origin__'):
            # Annotated type
            # Returns the instanstiated class of the bautype with the annotated type as py_type
            return cls._get_bautype(
                type.__origin__
            )(py_type=type)
        else:
            return type if issubclass(type, cls) else cls._get_bautypes()[type]

    @property
    def metadata(self):
        return dict(
            self.py_type.__metadata__[0]
        ) if hasattr(self.py_type,'__metadata__') else {}
    
@dataclass
class String(BauType):
    py_type: type = str
    db_type: type = sa.String
    ux_type: type = wtf.StringField

    def __post_init__(self):
        if hasattr(self.py_type,'__metadata__'):
            try:
                if self.py_type.__metadata__[0]['min_size'] > 100:
                    self.ux_type = wtf.TextAreaField
            except KeyError: pass

@dataclass
class Integer(BauType):
    py_type: type = int
    db_type: type = sa.Integer
    ux_type: type = wtf.IntegerField

@dataclass
class Float(BauType):
    py_type: type = float
    db_type: type = sa.Float
    ux_type: type = wtf.FloatField

@dataclass
class Bool(BauType):
    py_type: type = bool
    db_type: type = sa.Boolean
    ux_type: type = wtf.BooleanField

@dataclass
class Enum(BauType):
    py_type: type = tuple
    db_type: type = sa.Integer
    ux_type: type = wtf.SelectField

    #def py2ux(self):
    #    from enum import Enum
    #    "AnonymousEnum"

@dataclass
class DateTime(BauType):
    py_type: type = datetime.datetime
    db_type: type = sa.DateTime
    ux_type: type = wtf.DateTimeField

@dataclass
class Date(BauType):
    py_type: type = datetime.date
    db_type: type = sa.Date
    ux_type: type = wtf.DateField

@dataclass
class Time(BauType):
    py_type: type = datetime.time
    db_type: type = sa.Time
    ux_type: type = wtf.TimeField

@dataclass
class URL(BauType):
    py_type: type = url
    db_type: type = sa.String
    ux_type: type = wtf.StringField

    def ux2py(self):
        return urlparse(self.ux_item)

    def py2db(self):
        return self.py_item.geturl()
    
@dataclass
class File(BauType):
    py_type: type = Path
    db_type: type = sa.JSON
    ux_type: type = wtf.FileField

    def ux2py(self):
        import base64
        py_item = {
            'filename': self.ux_item.filename,
            'content_type': self.ux_item.content_type,
            'content_length': self.ux_item.content_length,
            'mimetype': self.ux_item.mimetype,
            'content': base64.b64encode(
                self.ux_item.stream.read()
            ).decode("utf-8")#errors="replace")
            # To decode back to bytes: 
        }
        return py_item
    
    def py2db(self):
        if (
            'storage_location' in self.metadata
        ) and (
            'content' in self.py_item
        ):
            
            import base64
            from flask import current_app
            from werkzeug.utils import secure_filename
            storage_location = self.metadata['storage_location']
            filename = '{}-{}'.format(
                    datetime.datetime.now().strftime("%Y%m%d-%H%M%S"),
                    secure_filename(self.py_item['filename'])
            )
            filepath = os.path.join(
                current_app.instance_path, storage_location, filename
            )
            with open(filepath, 'wb') as fs:
                fs.write(
                    base64.b64decode(self.py_item.pop('content'))
                )
            self.py_item['content_location'] = filepath
        return self.py_item

@dataclass
class JSON(BauType):
    py_type: type = dict
    db_type: type = sa.JSON
    ux_type: type = wtf.FormField
    
@dataclass
class Task(BauType):
    py_type: type = callable
    db_type: type = sa.JSON
    # For this type the ux_type is intended for display and not input
    ux_type: type = wtf.TextAreaField
    
@dataclass
class OneToManyList:
    quantity: int
    _self_reference_url: str
    _add_action: str = None

    def __str__(self):
        return str(self.quantity)

# class DateTimeField(Field):
#     def __init__(self, label=None, validators=None, **kwargs):
#         super().__init__(label, validators, **kwargs)
#         self.date_field = DateField(validators=[DataRequired()])
#         self.time_field = TimeField(validators=[DataRequired()])

#     def process_formdata(self, valuelist):
#         if valuelist and len(valuelist) == 2:
#             try:
#                 date_value = datetime.strptime(valuelist[0], "%Y-%m-%d").date()
#                 time_value = datetime.strptime(valuelist[1], "%H:%M").time()
#                 self.data = datetime.combine(date_value, time_value)
#             except ValueError:
#                 self.data = None
#                 raise ValueError("Invalid date/time format.")

@dataclass
class Bauhaus:
    name: str
    model: str
    type: BauType
    default: any = MISSING

    def build_ux_field(self, blueprint, FormClass):
        if self.type.py_type == list[int]:
            # One2many relationship cannot yet be instantiated if this instance does not yet exist
            return
        default_value = self.default
        if self.name.endswith('_id') and self.name[:-3] in blueprint.all_models:
            model = blueprint.all_models[self.name[:-3]]
            setattr(
                FormClass,
                self.name,
                wtf.SelectField(
                    self.name.replace('_',' ').capitalize(),
                    # lambda required default model as otherwise the last reference to model is used
                    choices=lambda model=model: [(i.id,i) for i in blueprint.db.session.query(model).all()]
                )
            ) # TODO allow blank option if default is None
        elif self.type.py_type == tuple[str]:
            setattr(
                FormClass,
                self.name,
                wtf.SelectField(
                    self.name.replace('_',' ').capitalize(),
                    choices=[(i,l) for i,l in enumerate(default_value)]
                )
            )
        else:
            setattr(
                FormClass,
                self.name,
                # Primitive types
                self.type.ux_type(
                    self.name.replace('_',' ').capitalize(),
                    validators=(
                        [] if self.type.py_type is bool else [
                            wtf.validators.Optional() if default_value is None
                            else wtf.validators.InputRequired()
                        ]
                    ),
                    default=None if default_value is MISSING else default_value
                )
            )
        
    def build_db_column(self, blueprint):
        if self.name.endswith('_id') and self.name[:-3] in blueprint.all_models and self.type.py_type is int:
            blueprint.model_properties[
                self.model
            ][self.name[:-3]] = relationship(
                blueprint.snake_to_camel(self.name[:-3])
            )
            return sa.Column(
                self.name, sa.Integer, sa.ForeignKey(self.name[:-3]+".id"),
                nullable = True if self.default is None else False
            )
        else: return sa.Column(
                self.name, self.type.db_type,
                default = None if self.default is MISSING else self.default,
                nullable = True if self.default is None else False
        )

@dataclass
class Route:
    url_suffix: str
    name: str = None
    roles: list[str]|bool = True
    view_function: callable = None
    defaults: dict = field(default_factory=dict)
    methods: tuple[str] = ('GET',)
    return_type: type = None
    menu_label: str = None
    submenu: str = None
    subsubmenu: str = None

    def __post_init__(self):
        if self.name and self.view_function:
            self.protect_view()

    def protect_view(self):
        from flask_iam import login_required, role_required
        if (self.roles in (None,True) or isinstance(self.roles,list)):
            if isinstance(self.roles,list): # Custom set role protection
                self.view = role_required(self.roles)(self.view_function)
            else: # Standard login_required protection

                self.view = login_required(self.view_function)
        else: self.view = self.view_function
        if self.return_type is None:
            self.return_type = self.view_function.__annotations__.get(
                'return',MISSING
            )

    def set_view_post_init(self, name, view_function):
        self.name = name
        self.view_function = view_function
        self.protect_view()
