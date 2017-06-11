import puz

p = puz.read('example.puz')

numbering = p.clue_numbering()

print 'Across'
for clue in numbering.across:
    answer = ''.join(
        p.solution[clue['cell'] + i]
        for i in range(clue['len']))
    print clue['num'], clue['clue'], '-', answer

print 'Down'
for clue in numbering.down:
    answer = ''.join(
        p.solution[clue['cell'] + i * numbering.width]
        for i in range(clue['len']))
    print clue['num'], clue['clue'], '-', answer

for row in range(p.height):
    cell = row * p.width
    # Substitute p.solution for p.fill to print the answers
    print ' '.join(p.fill[cell:cell + p.width])
