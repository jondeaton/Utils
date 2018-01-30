#include <iostream>
#include <map>
#include <string>

using namespace std;

map<char, int> counts;

void count_chars(map<char, int>& counts, const string& line) {
    for (const char& c : line) {
        if (counts.find(c) == counts.end()) counts[c] = 1;
        else counts[c]++;
    }
}

void print_chars(const map<char, int>& counts) {
    for (auto pair : counts)
        cout << pair.first << ": " << pair.second << endl;
}


int main() {
    map<char, int> counts;
    for(string line; getline(cin, line);)
        count_chars(counts, line);
    print_chars(counts);
    return 0;
}
