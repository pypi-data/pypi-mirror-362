class PowerFullInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def execute(self, source_code):
        lines = source_code.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if not line:
                i += 1
                continue

            if line.startswith("#PYTHON_START"):
                # Start reading embedded Python block
                python_block = []
                i += 1
                while i < len(lines):
                    if lines[i].strip().startswith("#PYTHON_END"):
                        break
                    python_block.append(lines[i])
                    i += 1
                # Join and run Python block
                python_code = "\n".join(python_block)
                exec(python_code, globals(), locals())
                i += 1
                continue

            if line.startswith("பதிப்பி") or line.startswith("எழுது"):
                to_print = line.split(" ", 1)[1]
                value = self.evaluate_expression(to_print)
                print(value)
            elif "=" in line:
                var, expr = line.split("=", 1)
                var = var.strip()
                expr = expr.strip()
                self.variables[var] = self.evaluate_expression(expr)
            elif line.startswith("ஆனால்"):
                condition = line[5:].strip(":").strip()
                if self.evaluate_expression(condition):
                    i += 1
                else:
                    while i < len(lines):
                        i += 1
                        if lines[i].strip().startswith("இல்லை"):
                            break
                        if not lines[i].strip():
                            break
                continue
            elif line.startswith("இல்லை"):
                i += 1
                continue
            elif line.startswith("ஆக"):
                parts = line[4:].strip(":").split()
                var = parts[0]
                start = int(parts[2])
                end = int(parts[4])
                block = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("முடி"):
                    block.append(lines[i])
                    i += 1
                for val in range(start, end):
                    self.variables[var] = val
                    for inner_line in block:
                        self.execute(inner_line)
            elif line.startswith("நிரல்பாகம்"):
                func_name = line.split()[1].strip(":")
                block = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("முடி"):
                    block.append(lines[i])
                    i += 1
                self.functions[func_name] = block
            elif line.startswith("அழை"):
                func_name = line.split()[1]
                if func_name in self.functions:
                    for func_line in self.functions[func_name]:
                        self.execute(func_line)
                else:
                    print(f"Unknown function: {func_name}")
            else:
                self.evaluate_expression(line)

            i += 1

    def evaluate_expression(self, expr):
        for var in self.variables:
            expr = expr.replace(var, str(self.variables[var]))
        try:
            return eval(expr)
        except Exception:
            return expr
