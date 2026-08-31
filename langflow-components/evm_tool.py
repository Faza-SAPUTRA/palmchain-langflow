from langflow.custom import Component
from langflow.inputs import MessageTextInput
from langflow.template import Output
from langflow.schema import Message
import json
from web3 import Web3
from langchain_core.tools import StructuredTool, Tool

# ABI dari PalmChain.sol (hanya function yang kita butuhkan)
PALMCHAIN_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "_assetId", "type": "string"}
        ],
        "name": "getAsset",
        "outputs": [
            {
                "components": [
                    {"internalType": "string", "name": "assetId", "type": "string"},
                    {"internalType": "string", "name": "petaniId", "type": "string"},
                    {"internalType": "string", "name": "namaPetani", "type": "string"},
                    {"internalType": "string", "name": "koperasi", "type": "string"},
                    {"internalType": "uint256", "name": "beratKg", "type": "uint256"},
                    {"internalType": "string", "name": "grade", "type": "string"},
                    {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
                    {"internalType": "string", "name": "status", "type": "string"}
                ],
                "internalType": "struct PalmChain.SawitAsset",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getAllAssetIds",
        "outputs": [
            {"internalType": "string[]", "name": "", "type": "string[]"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

class EVMSmartContractCaller(Component):
    display_name = "EVM PalmChain Tool"
    description = "Alat ini digunakan untuk mengambil data kelapa sawit dari Blockchain EVM. Panggil 'getAllAssetIds' untuk melihat daftar ID yang tersedia. Panggil 'getAsset' dengan asset_id untuk melihat detail spesifik."

    inputs = [
        MessageTextInput(
            name="rpc_url",
            display_name="RPC URL",
            info="URL endpoint node EVM",
            value="http://127.0.0.1:8545",
            advanced=True
        ),
        MessageTextInput(
            name="contract_address",
            display_name="Contract Address",
            info="Alamat Smart Contract",
            value="0x5FbDB2315678afecb367f032d93F642f64180aa3",
            advanced=True
        ),
        MessageTextInput(
            name="action",
            display_name="Action",
            info="Wajib diisi. Tulis 'getAllAssetIds' jika ingin melihat semua ID, atau 'getAsset' jika ingin melihat data spesifik."
        ),
        MessageTextInput(
            name="asset_id",
            display_name="Asset ID",
            info="Hanya diisi jika action adalah 'getAsset'. Masukkan ID (contoh: 'TBS-20260821-001').",
            value=""
        )
    ]
    
    outputs = [
        Output(display_name="Output Tool", name="output", method="execute_call", types=["Tool"]),
    ]

    def execute_call(self) -> Tool:
        def fetch_blockchain_data(action: str, asset_id: str = "") -> str:
            try:
                action = action.strip()
                asset_id = asset_id.strip() if asset_id else ""
                
                w3 = Web3(Web3.HTTPProvider(self.rpc_url))
                if not w3.is_connected():
                    return f"Error: Tidak bisa terhubung ke Blockchain di {self.rpc_url}"
                
                contract = w3.eth.contract(address=self.contract_address, abi=PALMCHAIN_ABI)
                
                if "getAllAssetIds" in action:
                    asset_ids = contract.functions.getAllAssetIds().call()
                    return f"Daftar Asset ID di Blockchain:\n{json.dumps(asset_ids, indent=2)}"
                    
                elif "getAsset" in action:
                    if not asset_id or asset_id == "" or asset_id == "None":
                        return "Error: Tolong berikan asset_id yang spesifik."
                    
                    try:
                        asset_data = contract.functions.getAsset(asset_id).call()
                        formatted_data = {
                            "assetId": asset_data[0],
                            "petaniId": asset_data[1],
                            "namaPetani": asset_data[2],
                            "koperasi": asset_data[3],
                            "beratKg": asset_data[4],
                            "grade": asset_data[5],
                            "timestamp": asset_data[6],
                            "status": asset_data[7]
                        }
                        if formatted_data["assetId"] == "":
                            return f"Asset dengan ID {asset_id} tidak ditemukan."
                            
                        return f"Data Blockchain:\n{json.dumps(formatted_data, indent=2)}"
                    except Exception as ex:
                         return f"Error saat getAsset({asset_id}): {str(ex)}"
                         
                else:
                    return f"Error: Action '{action}' tidak valid. Gunakan 'getAllAssetIds' atau 'getAsset'."
                    
            except Exception as e:
                return f"Blockchain Error: {str(e)}"
                
        # Return Langchain Tool
        return StructuredTool.from_function(
            func=fetch_blockchain_data,
            name="EVM_PalmChain_Tool",
            description="Alat untuk mengambil data kelapa sawit dari Blockchain EVM. Panggil 'getAllAssetIds' untuk melihat daftar ID yang tersedia. Panggil 'getAsset' dengan asset_id untuk melihat detail spesifik."
        )

