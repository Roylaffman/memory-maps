from fastkml import kml
from lxml import etree

kml_content = open('test_data/sample.kml', 'rb').read()

# Parse with lxml
tree = etree.fromstring(kml_content)
print(f"XML parsed successfully")
print(f"Root tag: {tree.tag}")

# Try fastkml with parse method
k = kml.KML()
k.from_string(kml_content)

print(f"\nKML features after from_string: {len(k.features)}")

# Try alternative: parse the tree directly
k2 = kml.KML.class_from_element(tree)
print(f"KML features after class_from_element: {len(k2.features) if k2 else 'None'}")

if k2 and k2.features:
    for feature in k2.features:
        print(f"\nFeature type: {type(feature)}")
        print(f"Feature name: {getattr(feature, 'name', 'N/A')}")
        if hasattr(feature, 'features'):
            print(f"Sub-features: {len(feature.features)}")
            for sub in feature.features:
                print(f"  - {getattr(sub, 'name', 'N/A')}: {type(sub)}")
                if hasattr(sub, 'geometry'):
                    print(f"    Geometry: {sub.geometry}")
