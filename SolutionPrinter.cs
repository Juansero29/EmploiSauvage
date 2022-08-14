using Google.OrTools.Sat;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EmploiSauvage
{
    public class SolutionPrinter : CpSolverSolutionCallback
    {
        public SolutionPrinter(int[] allNurses, int[] allDays, int[] allShifts,
                               Dictionary<(int, int, int), BoolVar> shifts, int limit)
        {
            solutionCount_ = 0;
            allNurses_ = allNurses;
            allDays_ = allDays;
            allShifts_ = allShifts;
            shifts_ = shifts;
            solutionLimit_ = limit;
        }

        public override void OnSolutionCallback()
        {
            Console.WriteLine($"Solution #{solutionCount_}:");
            foreach (int d in allDays_)
            {
                Console.WriteLine($"Day {d}");
                foreach (int n in allNurses_)
                {
                    bool isWorking = false;
                    foreach (int s in allShifts_)
                    {
                        if (Value(shifts_[(n, d, s)]) == 1L)
                        {
                            isWorking = true;
                            Console.WriteLine($"  Nurse {n} work shift {s}");
                        }
                    }
                    if (!isWorking)
                    {
                        Console.WriteLine($"  Nurse {d} does not work");
                    }
                }
            }
            solutionCount_++;
            if (solutionCount_ >= solutionLimit_)
            {
                Console.WriteLine($"Stop search after {solutionLimit_} solutions");
                StopSearch();
            }
        }

        public int SolutionCount()
        {
            return solutionCount_;
        }

        private int solutionCount_;
        private int[] allNurses_;
        private int[] allDays_;
        private int[] allShifts_;
        private Dictionary<(int, int, int), BoolVar> shifts_;
        private int solutionLimit_;
    }
}
