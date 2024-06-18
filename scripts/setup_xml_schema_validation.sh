#!/bin/bash
set -e

script_dir=$PWD
cd "$script_dir/.."
find Mods -name "UpgradeData.xml" -exec sed -Ei 's#^<Catalog>#<Catalog xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../../../../schemas/SchemaUpgradeData.xsd">#g' {} \;
find Maps -name "UpgradeData.xml" -exec sed -Ei 's#^<Catalog>#<Catalog xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../../../../../../schemas/SchemaUpgradeData.xsd">#g' {} \;
find Mods -name "RequirementData.xml" -exec sed -Ei 's#^<Catalog>#<Catalog xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../../../../schemas/SchemaRequirementData.xsd">#g' {} \;
find Maps -name "RequirementData.xml" -exec sed -Ei 's#^<Catalog>#<Catalog xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../../../../../../schemas/SchemaRequirementData.xsd">#g' {} \;
find Mods -name "RequirementNodeData.xml" -exec sed -Ei 's#^<Catalog>#<Catalog xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../../../../schemas/SchemaRequirementNodeData.xsd">#g' {} \;
find Maps -name "RequirementNodeData.xml" -exec sed -Ei 's#^<Catalog>#<Catalog xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../../../../../../schemas/SchemaRequirementNodeData.xsd">#g' {} \;
