'use client';

import { createContext, ReactNode, useContext, useState, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';

interface User {
  id: number;
  email: string;
  name: string;
}

interface AuthContextType {
  isAuth: boolean;
  user: User | null;
  login: (user: User) => void;
  logout: () => void;
  testLogin: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  
  const [isAuth, setIsAuth] = useState(false);
  const [user, setUser] = useState<User | null>(null);

  const login = (user: User) => {
    // TODO
    // localStorage.setItem("token", "...");
    // localStorage.setItem("user", JSON.stringify(user))
    // setIsAuth(true)
    // setUser(user);
    // router.push('/chat');
  };

  const testLogin = () => {
    localStorage.setItem("token", "dummytoken");
    localStorage.setItem("user", JSON.stringify({id: 1, email: "user1@example.com", name: "User1"}));
    setIsAuth(true)
    setUser({id: 1, email: "user1@example.com", name: "User1"} as User);
    router.push('/chat');
  }

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setIsAuth(false);
    setUser(null);
    router.push('/');
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (token && user) {
      setIsAuth(true);
      setUser(JSON.parse(user));
      
      if (pathname === '/') {
        router.push('/chat')
      }
    } else {
      setIsAuth(false)
      router.push('/')
    }
  }, []);

  return (
    <AuthContext.Provider value={{ isAuth, user, login, logout, testLogin }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
