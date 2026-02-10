# Run this cell
s = "computer"
print("s =", s)
print("s[0] =", s[0])
print("s[-1] =", s[-1])
print("s[1:4] =", s[1:4])
print("s[:3] =", s[:3])
print("s[3:] =", s[3:])

# Run this cell
s = "  Hello World  "
print("Original:", repr(s))
print("strip():", repr(s.strip()))
print("upper():", repr(s.upper()))

text = "red,green,blue"
colors = text.split(",")
print("split ->", colors)
print("join  ->", ",".join(colors))

print("'cat' in 'concatenate' ->", "cat" in "concatenate")
print("'computer'.startswith('com') ->", "computer".startswith("com"))
print("'computer'.endswith('ter')   ->", "computer".endswith("ter"))
