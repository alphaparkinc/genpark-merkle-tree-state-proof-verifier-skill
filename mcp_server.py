import sys, json
from client import MerkleTreeStateProofVerifier

verifier = MerkleTreeStateProofVerifier()

def handle_jsonrpc(line):
    global verifier
    try:
        req = json.loads(line)
        req_id = req.get("id")
        method = req.get("method")
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "genpark-merkle-tree-state-proof-verifier-skill", "version": "1.0.0"}, "capabilities": {"tools": {}}}}
        elif method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [
                {"name": "build_merkle_root", "description": "Compute Merkle root from leaves.", "inputSchema": {"type": "object", "properties": {"leaves": {"type": "array"}}, "required": ["leaves"]}},
                {"name": "verify_inclusion_proof", "description": "Verify leaf inclusion against Merkle root.", "inputSchema": {"type": "object", "properties": {"leaf": {"type": "string"}, "proof": {"type": "array"}, "root": {"type": "string"}}, "required": ["leaf", "proof", "root"]}},
                {"name": "benchmark_merkle_verification", "description": "Run standard Merkle benchmark.", "inputSchema": {"type": "object", "properties": {}}}
            ]}}
        elif method == "tools/call":
            params = req.get("params", {})
            tool = params.get("name")
            args = params.get("arguments", {})
            if tool == "build_merkle_root":
                root, _ = verifier.build_tree(args.get("leaves", []))
                res = {"root": root}
            elif tool == "verify_inclusion_proof":
                valid = verifier.verify_proof(args.get("leaf"), args.get("proof"), args.get("root"))
                res = {"verified": valid}
            elif tool == "benchmark_merkle_verification":
                res = verifier.benchmark_merkle_verification()
            else:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}

def main():
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_jsonrpc(line.strip())), flush=True)

if __name__ == "__main__":
    main()
