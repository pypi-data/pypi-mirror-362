import random
import string

def random_var_name(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

def weave_confusion(source_code: str) -> str:
    lines = source_code.splitlines()
    junk_snippets = [
        "pass",
        "x = 0",
        "y = 1",
        "z = x + y",
        "if False:\\n    pass",
        "try:\\n    pass\\nexcept:\\n    pass",
        "for _ in range(1):\\n    pass",
        "def {func}():\\n    return 42",
        "class {cls}:\\n    def method(self):\\n        pass",
        "lambda x: x + 1",
        "assert True",
        "with open('/dev/null', 'w') as f:\\n    f.write('junk')"
    ]
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if random.random() < 0.15:
            junk = random.choice(junk_snippets)
            if '{func}' in junk:
                junk = junk.format(func=random_var_name())
            if '{cls}' in junk:
                junk = junk.format(cls=random_var_name())
            new_lines.append(junk)
    return "\\n".join(new_lines)
