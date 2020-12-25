from curium import preprocessor

pre = preprocessor.PreProcessor()


pre.update("""
%define a bc
print(a,"a");
""")