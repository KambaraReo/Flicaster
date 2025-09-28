"use client";

import Link from "next/link";
import { Menu } from "lucide-react";
import { Sheet, SheetContent, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { TrendingUpDown, ChartLine } from "lucide-react";

const navItems = [
  {
    name: "単日LF予測",
    href: "/predict",
    icon: <TrendingUpDown className="w-5 h-5 mr-2" />,
  },
  {
    name: "LF予測推移",
    href: "/trend",
    icon: <ChartLine className="w-5 h-5 mr-2" />,
  },
];

const Sidebar = () => {
  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden md:flex flex-col w-60 bg-gradient-to-b from-blue-900 to-blue-950 text-white shadow-lg">
        <div className="p-4 text-2xl font-bold tracking-wide font-[fantasy]">
          Flicaster
        </div>
        <nav className="flex-1 px-2 space-y-2">
          {navItems.map((item) => (
            <Link
              key={item.name}
              href={item.href}
              className="block px-4 py-2 rounded-lg hover:bg-blue-700 transition"
            >
              <div className="flex items-center">
                {item.icon}
                {item.name}
              </div>
            </Link>
          ))}
        </nav>
      </aside>

      {/* Mobile Sidebar */}
      <div className="md:hidden fixed top-0 left-0 w-full flex items-center justify-between bg-blue-950 text-white px-4 py-3 shadow-md z-50">
        <div className="text-xl font-bold font-[fantasy]">Flicaster</div>
        <Sheet>
          <SheetTrigger>
            <Menu className="h-6 w-6" />
          </SheetTrigger>
          <SheetContent side="left" className="bg-blue-900 text-white">
            <SheetTitle className="sr-only">Navigation Menu</SheetTitle>
            <nav className="mt-6 space-y-4">
              {navItems.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="block px-4 py-2 rounded-lg hover:bg-blue-700 transition"
                >
                  <div className="flex items-center">
                    {item.icon}
                    {item.name}
                  </div>
                </Link>
              ))}
            </nav>
          </SheetContent>
        </Sheet>
      </div>
    </>
  );
};

export { Sidebar };
