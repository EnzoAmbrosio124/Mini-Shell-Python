#Enzo Ambrosio da Costa - 24008773
#João Vitor Guedes del Ducca - 24012015

import os
import sys
import platform
import subprocess
import multiprocessing

def cd(c): #Comando cd

    a = c.split()
    
    if len(a) == 2:
        d = a[1]
        
        try:
            os.chdir(d)
        
        except FileNotFoundError:
            print(f"erro: cd: {d}: Arquivo ou diretório não encontrado", file=sys.stderr)
        
        except NotADirectoryError:
            print(f"erro: cd: {d}: Não é um diretório", file=sys.stderr)
        
        except PermissionError:
            print(f"erro: cd: {d}: Permissão negada", file=sys.stderr)
        
        except Exception as e:
            print(f"erro: cd: {d}: {e}", file=sys.stderr)

def exec_cmd(c): #Processo filho
    
    arq_out = None
    c = c.strip()
    
    if ">" in c:
        p = c.split(">", 1)
        c = p[0].strip()
        arq_out = p[1].strip()
        
        if not arq_out:
            sys.stderr.write("erro: sintaxe inválida\n")
            sys.exit(2)

    if not c:
        if arq_out:
            open(arq_out, 'w').close()
        
        sys.exit(0)

    a = c.split()
    cmd = a[0]
    
    try:
        if arq_out:
            fd = os.open(arq_out, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o666)
            os.dup2(fd, sys.stdout.fileno())
            os.close(fd)

        #Comando pwd
        if cmd == "pwd":
            print(os.getcwd())
        
        #Comando ls
        elif cmd == "ls":
            for i in sorted(os.listdir(".")):
                print(i)
        
        #Comando cat - ex: cat EXE7.asm
        elif cmd == "cat":
            if len(a) == 2:
                try:
                    with open(a[1]) as f:
                        print(f.read(), end="")
                
                except FileNotFoundError:
                    print(f"erro: cat: {a[1]}: Arquivo ou diretório não encontrado", file=sys.stderr)
                
                except IsADirectoryError:
                    print(f"erro: cat: {a[1]}: É um diretório", file=sys.stderr)
                
                except Exception as e:
                    print(f"erro: cat: {a[1]}: {e}", file=sys.stderr)
            
            else:
                print("erro: cat: argumento inválido", file=sys.stderr)
        
        #Comando echo - ex: >echo "So Special VIVIZ"
        elif cmd == "echo":
            print(" ".join(a[1:]))
        
        #Comandos externos
        else:
            try:
                if platform.system() == "Windows":
                    r = subprocess.run(a, check=False)
                    sys.exit(r.returncode)
                
                else:
                    os.execvp(cmd, a)
            
            except FileNotFoundError:
                print(f"erro: {cmd}: comando não encontrado", file=sys.stderr)
                sys.exit(127)
            
            except PermissionError:
                print(f"erro: {cmd}: Permissão negada", file=sys.stderr)
                sys.exit(126)
            
            except Exception as e:
                print(f"erro: {cmd}: {e}", file=sys.stderr)
                sys.exit(1)
        
        sys.exit(0)
    
    except SystemExit:
        raise
    
    except Exception as e:
        print(f"Erro no processo filho: {e}", file=sys.stderr)
        sys.exit(125)

def shell():

    win = platform.system() == "Windows"
    
    while True:
        try:
            l = input("\n> ")
        
        except EOFError:
            print("sair")
            break
        
        except KeyboardInterrupt:
            print()
            continue

        e = l.strip()
        
        if not e:
            continue
        
        if e == "exit":
            break

        #Comando em sequencia (;) ex: echo "HOT"; echo "Come Over"; echo "Ash"; echo "So Cynical (Badum)"
        seqs = e.split(';')
        
        for s in seqs:
            s = s.strip()
            
            if not s:
                continue
            
            #Comando em paralelo (&) ex: ls & echo "Rebel Heart IVE"
            ps = s.split('&')
            ps_lst = []
            
            for c in ps:
                c = c.strip()
                
                if not c:
                    continue
                
                pri = c.split(">", 1)[0].strip()
                n = pri.split()[0]
                
                if pri:
                    n = pri.split()[0]
                
                else:
                    n = ""
                
                if n == "cd":
                    cd(pri)
                
                else:
                    if not win:
                        pid = os.fork()
                        
                        if pid == 0:
                            exec_cmd(c)
                        
                        else:
                            ps_lst.append(pid)
                    
                    else:
                        p = multiprocessing.Process(target=exec_cmd, args=(c,))
                        p.start()
                        ps_lst.append(p)
            
            for p in ps_lst:
                try:
                    if not win:
                        os.waitpid(p, 0)
                    
                    else:
                        p.join()
                
                except:
                    pass

if __name__ == "__main__":
    if platform.system() == "Windows":
        multiprocessing.freeze_support()
    
    shell()