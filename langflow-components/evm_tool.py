from langflow.custom import Component
from langflow.inputs import MessageTextInput
from langflow.template import Output
from langflow.schema import Message
import json
from web3 import Web3

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
    display_name = "EVM Contract Caller"
    description = "Memanggil fungsi di Smart Contract EVM berdasarkan JSON instruksi dari LLM."

    inputs = [
        MessageTextInput(
            name="rpc_url",
            display_name="RPC URL",
            info="URL endpoint node EVM (contoh: http://127.0.0.1:8545)",
            value="http://127.0.0.1:8545"
        ),
        MessageTextInput(
            name="contract_address",
            display_name="Contract Address",
            info="Alamat Smart Contract yang sudah di-deploy.",
            value="0x5FbDB2315678afecb367f032d93F642f64180aa3"
        ),
        MessageTextInput(
            name="llm_instruction",
            display_name="LLM Instruction (JSON)",
            info="Output JSON dari LLM",
            is_list=False
        )
    ]
    
    outputs = [
        Output(display_name="Message", name="output_message", method="execute_call"),
    ]

    def execute_call(self) -> Message:
        try:
            # 1. Parsing instruksi dari LLM
            llm_text = self.llm_instruction
            if hasattr(llm_text, "text"):
                llm_text = llm_text.text
            elif isinstance(llm_text, Message):
                llm_text = llm_text.text
            else:
                llm_text = str(llm_text)
            
            # Langflow kadang memberikan string kosong atau json block, kita bersihkan dulu
            llm_text = llm_text.strip()
            if llm_text.startswith("```json"):
                llm_text = llm_text.replace("```json", "").replace("```", "").strip()
                
            instruction = json.loads(llm_text)
            action = instruction.get("action")
            
            # 2. Setup koneksi Web3
            w3 = Web3(Web3.HTTPProvider(self.rpc_url))
            if not w3.is_connected():
                return Message(text=f"Blockchain Connection Error: Tidak bisa terhubung ke {self.rpc_url}")
            
            # 3. Load Smart Contract
            contract = w3.eth.contract(address=self.contract_address, abi=PALMCHAIN_ABI)
            
            # 4. Eksekusi berdasarkan instruksi LLM
            if action == "getAllAssetIds":
                asset_ids = contract.functions.getAllAssetIds().call()
                return Message(text=f"Daftar Asset ID di Blockchain:\n{json.dumps(asset_ids, indent=2)}")
                
            elif action == "getAsset":
                asset_id = instruction.get("assetId")
                if not asset_id:
                    return Message(text="Error: LLM tidak memberikan assetId untuk dipanggil.")
                
                try:
                    asset_data = contract.functions.getAsset(asset_id).call()
                    # Mapping tuple ke dictionary agar enak dibaca
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
                    # Filter empty string jika aset tidak ketemu (di EVM string kosong = tidak ada)
                    if formatted_data["assetId"] == "":
                        return Message(text=f"Asset dengan ID {asset_id} belum terdaftar di Blockchain.")
                        
                    return Message(text=f"Data Asset Blockchain:\n{json.dumps(formatted_data, indent=2)}")
                except Exception as ex:
                     return Message(text=f"Error saat getAsset({asset_id}): {str(ex)}")
                     
            else:
                return Message(text=f"Error: Aksi '{action}' tidak dikenali oleh Smart Contract Caller.")
                
        except json.JSONDecodeError:
             return Message(text=f"LLM tidak mengembalikan JSON yang valid. Pastikan output LLM berupa JSON.")
        except Exception as e:
            return Message(text=f"Terjadi kesalahan saat memanggil Smart Contract: {str(e)}")
