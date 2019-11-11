import scrape

file = open("output.csv")
out = open("output1.csv", "w")
out.write("Company Name, Category, Contact\n")

for line in file.readlines()[1:]:
    try:
        data = line.split(",")
        contact_link = data[2]
        contact_link = scrape.get_contact_us_link(contact_link)
        out.write(data[0]+","+data[1]+","+contact_link+"\n")
    except:
        out.write(line+"\n")
out.close()