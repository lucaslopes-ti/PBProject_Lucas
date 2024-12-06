def conta_vogais(s):
    vogal = lambda x: x.lower() in 'aeiou'
    
    vogais = filter(vogal, s)
    
    return len(list(vogais))
    


texto = "Exemplo de String com varias vogais"
print(conta_vogais(texto))
    