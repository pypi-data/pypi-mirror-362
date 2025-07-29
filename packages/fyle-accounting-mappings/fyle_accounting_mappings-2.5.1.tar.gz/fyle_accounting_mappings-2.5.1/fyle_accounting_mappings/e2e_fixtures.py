from django.utils import timezone
from datetime import datetime, timedelta

from .models import (
    MappingSetting, EmployeeMapping, CategoryMapping, Mapping,
    ExpenseAttribute, DestinationAttribute
)

class BaseFixtureFactory:
    """Base factory for creating test fixture data, common to all integrations."""

    def create_expense_attributes(self, workspace, count=5):
        """Create sample expense attributes"""
        attributes = []
        attribute_types = ['CATEGORY', 'PROJECT', 'COST_CENTER', 'EMPLOYEE', 'VENDOR']

        for i, attr_type in enumerate(attribute_types[:count]):
            attr = ExpenseAttribute.objects.create(
                workspace=workspace,
                attribute_type=attr_type,
                display_name=f'E2E {attr_type.title()}',
                value=f'e2e-{attr_type.lower()}-{i}',
                source_id=f'src_{i}',
                detail={'description': f'E2E test {attr_type.lower()}'},
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            attributes.append(attr)

        return attributes

    def create_destination_attributes(self, workspace, count=5):
        """Create sample destination attributes"""
        attributes = []
        attribute_types = [
            'ACCOUNT', 'VENDOR', 'EMPLOYEE', 'LOCATION', 'DEPARTMENT'
        ]

        for i, attr_type in enumerate(attribute_types[:count]):
            attr = DestinationAttribute.objects.create(
                workspace=workspace,
                attribute_type=attr_type,
                display_name=f'E2E {attr_type.title()} {i+1}',
                value=f'e2e-{attr_type.lower()}-{i+1}',
                destination_id=f'dst_{i+1}',
                detail={'code': f'E2E{i+1}'},
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            attributes.append(attr)

        return attributes

    def create_mapping_settings(self, workspace, count=3):
        """Create sample mapping settings"""
        settings = []
        setting_types = ['EMPLOYEE', 'CATEGORY', 'PROJECT']

        for i, setting_type in enumerate(setting_types[:count]):
            setting = MappingSetting.objects.create(
                workspace=workspace,
                source_field=setting_type,
                destination_field='VENDOR' if setting_type == 'EMPLOYEE' else 'ACCOUNT',
                import_to_fyle=True,
                is_custom=False,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            settings.append(setting)

        return settings

    def create_mappings(self, workspace, expense_attrs, dest_attrs, count=1):
        """Create sample mappings using source_id FK to ExpenseAttribute"""
        mappings = []

        for i in range(count):
            # Get source and destination attributes
            source_attr = expense_attrs[i % len(expense_attrs)]
            dest_attr = dest_attrs[i % len(dest_attrs)]

            mapping = Mapping.objects.create(
                workspace=workspace,
                source_type='EMPLOYEE',
                destination_type='VENDOR',
                source=source_attr,  # FK to ExpenseAttribute
                destination=dest_attr,  # FK to DestinationAttribute
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            mappings.append(mapping)

        return mappings

    def create_employee_mappings(self, workspace, expense_attrs, dest_attrs, count=3):
        """Create sample employee mappings using source_employee FK"""
        mappings = []

        # Filter for employee attributes
        employee_attrs = [attr for attr in expense_attrs if attr.attribute_type == 'EMPLOYEE']
        vendor_attrs = [attr for attr in dest_attrs if attr.attribute_type == 'VENDOR']
        employee_dest_attrs = [attr for attr in dest_attrs if attr.attribute_type == 'EMPLOYEE']

        for i in range(min(count, len(employee_attrs))):
            source_employee = employee_attrs[i] if i < len(employee_attrs) else employee_attrs[0]
            dest_vendor = vendor_attrs[i % len(vendor_attrs)] if vendor_attrs else None
            dest_employee = employee_dest_attrs[i % len(employee_dest_attrs)] if employee_dest_attrs else None

            mapping = EmployeeMapping.objects.create(
                workspace=workspace,
                source_employee=source_employee,  # FK to ExpenseAttribute
                destination_vendor=dest_vendor,  # FK to DestinationAttribute
                destination_employee=dest_employee,  # FK to DestinationAttribute
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            mappings.append(mapping)

        return mappings

    def create_category_mappings(self, workspace, expense_attrs, dest_attrs, count=3):
        """Create sample category mappings using source_category FK"""
        mappings = []

        # Filter for category attributes
        category_attrs = [attr for attr in expense_attrs if attr.attribute_type == 'CATEGORY']
        account_attrs = [attr for attr in dest_attrs if attr.attribute_type == 'ACCOUNT']

        for i in range(min(count, len(category_attrs))):
            source_category = category_attrs[i] if i < len(category_attrs) else category_attrs[0]
            dest_account = account_attrs[i % len(account_attrs)] if account_attrs else None

            mapping = CategoryMapping.objects.create(
                workspace=workspace,
                source_category=source_category,  # FK to ExpenseAttribute
                destination_account=dest_account,  # FK to DestinationAttribute
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            mappings.append(mapping)

        return mappings
