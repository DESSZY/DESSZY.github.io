def gcd(a, b):
  while b:
    a, b = b, a % b
  return a

def parse_seximal(s):
  s = s.strip()
  neg = s.startswith("-")
  if neg:
    s = s[1:]
  parts = s.split(".")
  whole = parts[0] if parts[0] else "0"
  frac = parts[1] if len(parts) > 1 else ""
  
  num = 0
  for ch in whole:
    d = int(ch)
    if d >= 6:
      raise ValueError("Use 0-5 only")
    num = num * 6 + d
    
  den = 1
  for ch in frac:
    d = int(ch)
    if d >= 6:
      raise ValueError("Use 0-5 only")
    num = num * 6 + d
    den *= 6
    
  if neg:
    num = -num
  g = gcd(abs(num), den)
  return num // g, den // g

def to_seximal(num, den, places=10):
  if den == 0:
    return "Err: Div by 0"
  neg = (num < 0) ^ (den < 0)
  num, den = abs(num), abs(den)
  whole = num // den
  rem = num % den
  
  digits = []
  if whole == 0:
    digits.append("0")
  else:
    while whole > 0:
      digits.append(str(whole % 6))
      whole //= 6
    digits.reverse()
    
  res = ("-" if neg else "") + "".join(digits)
  if rem == 0:
    return res
    
  res += "."
  for _ in range(places):
    if rem == 0:
      break
    rem *= 6
    res += str(rem // den)
    rem %= den
  return res

ans_n, ans_d = 0, 1

while True:
  expr = input("> ").strip()
  if not expr:
    continue
  if expr.lower() == "q":
    break
  try:
    # Support chaining off Ans (e.g. "+ 5" or "* 2")
    if expr[0] in ["+", "-", "*", "/"] and len(expr) > 1 and expr[1] != ".":
      if not (expr[0] == "-" and expr[1:].replace(".", "").isdigit()):
        op = expr[0]
        n1, d1 = ans_n, ans_d
        n2, d2 = parse_seximal(expr[1:])
        if op == "+":
          ans_n, ans_d = n1 * d2 + n2 * d1, d1 * d2
        elif op == "-":
          ans_n, ans_d = n1 * d2 - n2 * d1, d1 * d2
        elif op == "*":
          ans_n, ans_d = n1 * n2, d1 * d2
        elif op == "/":
          ans_n, ans_d = n1 * d2, d1 * n2
        print("= " + to_seximal(ans_n, ans_d))
        continue

    for op in ["+", "-", "*", "/"]:
      if op in expr[1:]:
        idx = expr.find(op, 1)
        n1, d1 = parse_seximal(expr[:idx])
        n2, d2 = parse_seximal(expr[idx+1:])
        if op == "+":
          ans_n, ans_d = n1 * d2 + n2 * d1, d1 * d2
        elif op == "-":
          ans_n, ans_d = n1 * d2 - n2 * d1, d1 * d2
        elif op == "*":
          ans_n, ans_d = n1 * n2, d1 * d2
        elif op == "/":
          ans_n, ans_d = n1 * d2, d1 * n2
        print("= " + to_seximal(ans_n, ans_d))
        break
    else:
      ans_n, ans_d = parse_seximal(expr)
      print("Dec: " + str(ans_n / ans_d))
  except Exception as e:
    print("Err:", e)
