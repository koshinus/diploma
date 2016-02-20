//#include<iostream>

class test_class
{
public:
	virtual const char* a_show() = 0;
};

class b : public test_class
{
public:
	virtual const char* a_show(){ return "ba\n";};
	const char* b_show(){ return "b\n";};
};

class c : public test_class
{
public:
	virtual const char* a_show(){ return "ca\n";};
	const char* c_show(){ return "c\n";};
};

class d : public c
{
public:
	virtual const char* a_show(){ return "da\n";};
	const char* d_show(){ return "d\n";};
};

class e
{
public:
	virtual const char* e_show(){ return "e\n";};
};

class f : public e
{
public:
	virtual const char* e_show(){ return "fe\n";};
	const char* f_show(){ return "f\n";};
};

class g : public e
{
public:
	virtual const char* e_show(){ return "ge\n";};
	const char* g_show(){ return "g\n";};
};

class h : public g
{
public:
	virtual const char* e_show(){ return "he\n";};
	const char* h_show(){ return "h\n";};
};

class hd : public h, public d
{
public:
	static const int check_int = 8042342;
	double check_double;
	virtual const char* e_show(){ return "hde\n";};
	virtual const char* a_show(){ return "hda\n";};
	const char* hd_show(){ return "hd\n";};
};

int main()
{
	hd hd1;
	/*std::cout << hd1.a_show();
	std::cout << hd1.c_show();
	std::cout << hd1.d_show();
	std::cout << hd1.e_show();
	std::cout << hd1.g_show();
	std::cout << hd1.h_show();
	int n;
	std::cin >> n;*/
	return 0;
}
