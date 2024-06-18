#!/bin/bash
set -e

script_dir=$PWD
cd "$script_dir/.."
find . -name "UpgradeData.xml" -exec sed -Ei 's#^<Catalog>#<Catalog xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../../../../schemas/SchemaUpgradeData.xsd">#g' {} \;
find . -name "RequirementData.xml" -exec sed -Ei 's#^<Catalog>#<Catalog xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../../../../schemas/SchemaRequirementData.xsd">#g' {} \;
find . -name "RequirementNodeData.xml" -exec sed -Ei 's#^<Catalog>#<Catalog xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../../../../schemas/RequirementNodeData.xsd">#g' {} \;
