const hre = require("hardhat");

async function main() {
  const PalmChain = await hre.ethers.getContractFactory("PalmChain");
  const palmChain = await PalmChain.deploy();

  await palmChain.waitForDeployment();

  console.log("PalmChain deployed to:", await palmChain.getAddress());

  console.log("Inserting dummy data...");
  
  const tx1 = await palmChain.recordAsset(
    "TBS-20260821-001",
    "P-001",
    "Budi Santoso",
    "Koperasi Sukamaju",
    2545,
    "A",
    "COLLECTED"
  );
  await tx1.wait();

  const tx2 = await palmChain.recordAsset(
    "TBS-20260821-002",
    "P-002",
    "Siti Aminah",
    "Koperasi Mandiri",
    1800,
    "B",
    "COLLECTED"
  );
  await tx2.wait();

  console.log("Dummy data inserted successfully!");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
