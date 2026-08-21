// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract PalmChain {
    struct SawitAsset {
        string assetId;
        string petaniId;
        string namaPetani;
        string koperasi;
        uint256 beratKg; // weight in kg (scaled by 10 to handle 1 decimal)
        string grade;
        uint256 timestamp;
        string status;
    }

    mapping(string => SawitAsset) public assets;
    string[] public assetIds;

    event AssetRecorded(string assetId, string petaniId, uint256 beratKg, string koperasi);

    function recordAsset(
        string memory _assetId,
        string memory _petaniId,
        string memory _namaPetani,
        string memory _koperasi,
        uint256 _beratKg,
        string memory _grade,
        string memory _status
    ) public {
        require(bytes(assets[_assetId].assetId).length == 0, "Asset ID already exists");

        assets[_assetId] = SawitAsset({
            assetId: _assetId,
            petaniId: _petaniId,
            namaPetani: _namaPetani,
            koperasi: _koperasi,
            beratKg: _beratKg,
            grade: _grade,
            timestamp: block.timestamp,
            status: _status
        });

        assetIds.push(_assetId);
        emit AssetRecorded(_assetId, _petaniId, _beratKg, _koperasi);
    }

    function getAsset(string memory _assetId) public view returns (SawitAsset memory) {
        require(bytes(assets[_assetId].assetId).length != 0, "Asset not found");
        return assets[_assetId];
    }

    function getAllAssetIds() public view returns (string[] memory) {
        return assetIds;
    }
}
