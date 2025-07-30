import json
import re

def infer_value_type(value: str, labels=None):
	value = value.strip()
	if value.startswith("[") and value.endswith("]") and labels:
		return resolve_reference(value, labels)

	if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
		return value[1:-1]
	elif value.lower() == "true":
		return True
	elif value.lower() == "false":
		return False
	else:
		try:
			return float(value) if '.' in value else int(value)
		except ValueError:
			return value

def resolve_reference(value, labels):
	ref = value[1:-1].strip()
	if "." in ref:
		scope, identity = ref.split(".", 1)
		if ":" in scope:
			lbl, sp = scope.split(":", 1)
			data = labels[lbl][sp]
		else:
			data = labels[scope]
		return data.get(identity)
	elif ":" in ref:
		lbl, sp = ref.split(":", 1)
		return labels[lbl][sp]
	else:
		return labels[ref]

def parse_loon_file(filename, labels=None, spaces=None):
	if labels is None:
	   labels = {}
	if spaces is None:
		spaces = {}
	with open(filename, "r") as file:
		if not filename.endswith(".loon"):
			print("ERROR: file must be a .loon file")
			exit()
		code = [line.strip() for line in file if line.strip() and not line.strip().startswith("<")]
	current_label = None
	current_space = None
	label_stack = {}
	space_stack = {}
	insert_in_space = False

	for line in code:
		if line.startswith("(") and line.endswith(")"):
			current_label = line[1:-1]
			label_stack[current_label] = []
			current_space = None
			insert_in_space = False

		elif line.startswith(":"):
			current_space = line[1:]
			space_stack[current_space] = None
			insert_in_space = True

		elif line == "end:":
			result = space_stack[current_space]
			label_stack[current_label].append((current_space, result))
			spaces[current_space] = result
			insert_in_space = False
			current_space = None

		elif line == "end":
		    result = {}
		    for item in label_stack[current_label]:
		        if isinstance(item, tuple):
		            key, val = item
		            result[key] = val
		        elif isinstance(item, dict):
		            result.update(item)
		        elif isinstance(item, str):
		            result[item] = None
		    labels[current_label] = result
		    current_label = None

		elif "=" in line:
			k, v = map(str.strip, line.split("=", 1))
			val = infer_value_type(v, labels)
			if insert_in_space:
				blk = space_stack[current_space]
				if blk is None:
					blk = {}
					space_stack[current_space] = blk
				elif isinstance(blk, list):
					raise Exception(f"Cannot mix key-value with list in space '{current_space}'")
				blk[k] = val
			else:
				label_stack[current_label].append({k: val})
		elif line.startswith("@"):
		    file_name = line[1:]
		    if not file_name.endswith(".loon"):
		        print("ERROR: file must be a .loon file")
		        exit()
		    temp_labels = {}
		    parsed_import_file = parse_loon_file(file_name, temp_labels, spaces)
		    if current_label is None:
		        labels.update(parsed_import_file)
		    else:
		        if insert_in_space:
		            blk = space_stack[current_space]
		            if blk is None:
		                blk = []
		                space_stack[current_space] = blk
		            elif isinstance(blk, list):
		                raise Exception(f"Cannot mix key-value with list in space '{current_space}'")
		            blk.append({current_label: parsed_import_file})
		        else:
		            label_stack[current_label].append(parsed_import_file)
		    continue
		elif not line.startswith("->"):
			val = infer_value_type(line, labels)
			if insert_in_space:
				blk = space_stack[current_space]
				if blk is None:
					blk = []
					space_stack[current_space] = blk
				elif isinstance(blk, dict):
					blk = [{k: v} for k, v in blk.items()]
					space_stack[current_space] = blk
				blk.append(val)
			else:
				label_stack[current_label].append(val)

		elif line.startswith("->"):
			raw = line[2:].strip()
			is_value_only = raw.endswith("&")
			if is_value_only:
				raw = raw[:-1].strip()

			if "." in raw:
				scope, identity = raw.split(".", 1)
				if ":" in scope:
					lbl, sp = scope.split(":", 1)
					data = labels[lbl][sp]
				else:
					data = labels[scope]
				val = data.get(identity)
				injected = val if is_value_only else {identity: val}

			elif ":" in raw:
				lbl, sp = raw.split(":", 1)
				data = labels[lbl][sp]
				injected = data if is_value_only else {sp: data}

			else:
				data = labels[raw]
				injected = data if is_value_only else {raw: data}

			if insert_in_space:
				blk = space_stack[current_space]
				if is_value_only:
					if blk is None:
						blk = []
						space_stack[current_space] = blk
					elif isinstance(blk, dict):
						blk = [{k: v} for k, v in blk.items()]
						space_stack[current_space] = blk
					blk.append(injected)
				else:
					if blk is None:
						blk = {}
						space_stack[current_space] = blk
					elif isinstance(blk, list):
						raise Exception(f"Cannot mix structured injection with list in space '{current_space}'")
					blk.update(injected)
			else:
				label_stack[current_label].append(injected)

	return labels
