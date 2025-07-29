import logging

from tabulate import tabulate

from edmgr.utils import convert_bytes_size

logger = logging.getLogger(__name__)


def _format_table(serializer, items: list[dict], **kwargs) -> str:
    items = [serializer(item, **kwargs) for item in items]
    return tabulate(
        items, headers="keys", tablefmt=kwargs.get("tablefmt", "fancy_grid")
    )


def _format_country(country: dict, with_link: bool = False) -> str:
    link = country.get("uri")
    link_str = f" - {link}" if with_link else ""
    return f"{country.get('id', 'None').upper()}{link_str}"


def serialize_entitlement(entitlement: dict, **kwargs) -> dict:
    product = entitlement.get("product", {})
    characteristics = entitlement.get("characteristics", {})
    qualities = ", ".join(
        [e.get("quality") for e in entitlement.get("rights", {}).get("qualities", {})]
    )
    grouped = characteristics.get("grouped")
    virtual = characteristics.get("virtual")
    lic = "free" if characteristics.get("free") else "entitled"
    if grouped:
        virtual_entilements_len = len(entitlement.get("virtualEntitlements", []))
        entitlement_type = f"group ({virtual_entilements_len} entitlements)"
    elif virtual:
        entitlement_type = "virtual entitlement"
    else:
        entitlement_type = "entitlement"

    compliance = entitlement.get("compliance", {})
    us_eccn = ", ".join(compliance.get("usECCN", []))
    return {
        "ID": entitlement.get("id"),
        "Type": entitlement_type,
        "Product Code": product.get("id"),
        "Product Name": product.get("name"),
        "Status": entitlement.get("status"),
        "License": lic,
        "Right To": entitlement.get("rightTo"),
        "Valid From": entitlement.get("validFrom"),
        "Valid To": entitlement.get("validTo"),
        "Qualities": qualities,
        "ECCN(s)": us_eccn,
    }


def serialize_virtual_entitlements(virtual_entitlement: dict, **kwargs) -> dict:
    product = virtual_entitlement.get("product", {})
    foundries = product.get("foundry", [])
    return {
        "ID": virtual_entitlement.get("id"),
        "Product Code": product.get("id"),
        "Product Name": product.get("name"),
        "Product URI": product.get("uri"),
        "Foundries": ", ".join(foundries),
        "Process": product.get("process"),
    }


def serialize_release(release: dict, **kwargs) -> dict:
    return {
        "ID": release.get("id"),
        "Entitlement ID": release.get("entitlement", {}).get("id"),
        "Release Name": release.get("name"),
        "Revision": release.get("revision"),
        "Patch": release.get("patch"),
        "Major": release.get("majorVersion"),
        "Minor": release.get("minorVersion"),
        "Quality": release.get("quality"),
        "Type": release.get("type"),
        "Available At": release.get("availableAt"),
    }


def serialize_artifact(artifact: dict, **kwargs) -> dict:
    size = artifact.get("fileSize")
    bytes_size = convert_bytes_size(size, **kwargs) if size is not None else None
    return {
        "ID": artifact.get("id"),
        "Name": artifact.get("name"),
        "Description": artifact.get("description"),
        "Type": artifact.get("type"),
        "File Name": artifact.get("fileName"),
        "File Size": bytes_size,
        "MD5": artifact.get("md5"),
    }


def format_entitlements(entitlements: list[dict], **kwargs) -> str:
    return _format_table(serialize_entitlement, entitlements, **kwargs)


def format_releases(releases: list[dict], **kwargs) -> str:
    return _format_table(serialize_release, releases, **kwargs)


def format_artifacts(artifacts: list[dict], **kwargs) -> str:
    return _format_table(serialize_artifact, artifacts, **kwargs)


def format_entitlement(entitlement: dict, **kwargs) -> str:
    offset = kwargs.get("offset")
    product_code = kwargs.get("product_code")
    entitlement_view = serialize_entitlement(entitlement, **kwargs)
    compliance = entitlement.get("compliance", {})
    rights = entitlement.get("rights", {})
    history = entitlement.get("history", {})
    product = entitlement.get("product", {})
    countries = "\n".join(
        [
            _format_country(country, with_link=True)
            for country in compliance.get("allowedCountries", {})
        ]
    )
    us_eccn = ", ".join(compliance.get("usECCN", []))
    enhanced_entitlement_view = {
        "ID": entitlement_view["ID"],
        "Type": entitlement_view["Type"],
        "Product Code": entitlement_view["Product Code"],
        "Product Name": product.get("name"),
        "Product URI": product.get("uri"),
        "Status": entitlement_view["Status"],
        "License": entitlement_view["License"],
        "Right To": entitlement_view["Right To"],
        "Valid From": entitlement_view["Valid From"],
        "Valid To": entitlement_view["Valid To"],
        "Qualities": entitlement_view["Qualities"],
        "Allowed Countries": countries,
        "Compliance Status": compliance.get("status"),
        "Compliance Reason": compliance.get("statusReason"),
        "ECCN Restricted": compliance.get("eccnRestricted"),
        "ECCN(s)": us_eccn,
        "Maintenance From": rights.get("maintenanceFrom"),
        "Maintenance To": rights.get("maintenanceTo"),
        "Created At": history.get("createdAt"),
        "Last Changed": history.get("lastChangedAt"),
    }
    design_start_rights = rights.get("designStart")
    if design_start_rights:
        foundries = ", ".join([right.get("foundry") for right in design_start_rights])
        enhanced_entitlement_view = {
            **enhanced_entitlement_view,
            "Foundries": foundries,
        }
    output = tabulate(
        enhanced_entitlement_view.items(), tablefmt=kwargs.get("tablefmt", "fancy_grid")
    )
    virtual_entitlements = entitlement.get("virtualEntitlements", [])
    if product_code is not None and virtual_entitlements:
        virtual_entitlements = list(
            filter(lambda x: x["product"]["id"] == product_code, virtual_entitlements)
        )
        if not virtual_entitlements:
            output += f"No Entitlement were found for Product Code {product_code}"
    total_virtual_entitlements = len(virtual_entitlements)
    page = 1
    limit = total_virtual_entitlements
    if offset is not None:
        page = max(int(offset), page)
        limit = min(int(kwargs["limit"]), limit)
    start = (page - 1) * limit
    end = min(page * limit, total_virtual_entitlements)
    if total_virtual_entitlements:
        if start < end:
            sliced_virtual_entitlements = virtual_entitlements[start:end]
            output += (
                "\n\n"
                f"Showing from {start + 1} to {end} of {total_virtual_entitlements} "
                "Entitlements found:\n\n"
            )
            output += _format_table(
                serialize_virtual_entitlements,
                sliced_virtual_entitlements,
                **kwargs,
            )
        else:
            output += (
                "\n\nEntitlements page out of range. "
                f"Please check offset ({offset}) and/or limit ({limit}) options. "
                f"Total number of Entitlements found is {total_virtual_entitlements}"
                "\n\n"
            )
    return output
