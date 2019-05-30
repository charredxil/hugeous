import subprocess
import json
from tempfile import NamedTemporaryFile
from .models import Reason


def all_reason_names():
    names = [("", "")]
    for obj in Reason.objects.values("name"):
        names.append((obj["name"], obj["name"]))
    return names


def make_proof(rs, reason_names=True):
    if reason_names:
        return [[Reason.objects.get(name=rname).json, s] for rname, s in list(rs)]
    return [[r.json, s] for r, s in list(rs)]


def load_base_reasons():
    outfile = NamedTemporaryFile()
    subprocess.call(["prover-exe", "base", outfile.name])
    with open(outfile.name, "r") as f:
        data = json.load(f)
    for reason_json in data:
        save_reason(reason_json)


def save_reason(reason_json):
    name = reason_json["_name"] if "_name" in reason_json else None
    if reason_json["tag"] == "Given":
        name = "Given"
    elif reason_json["tag"] == "Substitution":
        name = "Substitution Property of Equality"
    if not Reason.objects.filter(name=name).exists():
        reason = Reason(name=name, json=reason_json)
        reason.save()


def verify(proof):
    infile = NamedTemporaryFile()
    outfile = NamedTemporaryFile()
    with open(infile.name, "w") as f:
        json.dump(proof, f)
    subprocess.call(["prover-exe", "verify", infile.name, outfile.name])
    with open(outfile.name, "r") as f:
        data = json.load(f)
    return data


def theorize(name, plist):
    infile = NamedTemporaryFile()
    outfile = NamedTemporaryFile()
    with open(infile.name, "w") as f:
        json.dump([name, plist], f)
    subprocess.call(["prover-exe", "theorize", infile.name, outfile.name])
    with open(outfile.name, "r") as f:
        data = json.load(f)
    return data


def postulate(name, plist):
    infile = NamedTemporaryFile()
    outfile = NamedTemporaryFile()
    with open(infile.name, "w") as f:
        json.dump([name, plist], f)
    subprocess.call(["prover-exe", "postulate", infile.name, outfile.name])
    with open(outfile.name, "r") as f:
        data = json.load(f)
    return data
